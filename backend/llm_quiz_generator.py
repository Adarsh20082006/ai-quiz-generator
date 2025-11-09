# llm_quiz_generator.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import QuizOutput
from vector_service import build_faiss_index
from langchain_core.runnables import RunnableSequence

load_dotenv()

# Initialize Output Parser
parser = PydanticOutputParser(pydantic_object=QuizOutput)
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
# Initialize Gemini Model (Stable, Fast)
model = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.5
)

def generate_quiz(article_title: str, structured_content: dict, difficulty="Medium", selected_sections=None):
    """Generate a factual, structured quiz from Wikipedia article content."""
    
    # Step 1: Extract relevant sections
    sections = structured_content.get("sections", [])
    if selected_sections:
        sections = [s for s in sections if s["heading"] in selected_sections]

    # Step 2: Merge content from sections + subsections
    article_text = "\n".join(
        (s.get("content", "")) + " " + " ".join(sub.get("content", "") for sub in s.get("subsections", []))
        for s in sections
    )

    # Building FAISS index for semantic relevance
    vector_store, _ = build_faiss_index(article_text)
    query = f"important facts, achievements, and insights about {article_title}"
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    docs = retriever.invoke(query)
    relevant_text = "\n".join([d.page_content for d in docs])

    # Creating the prompt
    prompt = PromptTemplate(
        input_variables=["title", "content", "difficulty"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
        template="""

        You are an expert Educational Content Designer and a meticulous Fact-Checker.
        Your *sole* purpose is to transform a provided source text into a high-quality, structured JSON quiz.
        Your primary directive is 100% factual accuracy and strict, unwavering adherence to the provided source text.

        <Article Title>
        {title}
        </Article Title>

        <SOURCE_TEXT>
        {content}
        </SOURCE_TEXT>

        <JSON_SCHEMA>
        {format_instructions}
        </JSON_SCHEMA>

        <CONFIG>
        Difficulty Mode: {difficulty}
        </CONFIG>

        <CORE_PRINCIPLES>
        1.  **Zero-Knowledge Mandate:** You MUST assume you have ZERO knowledge of the world, history, or any facts *outside* the provided `<SOURCE_TEXT>`.
        2.  **Strict Grounding:** Every single piece of generated output (question, answer, explanation, entity) MUST be 100% derivable *directly* from the `<SOURCE_TEXT>`.
        3.  **No Inference:** You MUST NOT infer, guess, or create logical connections between facts that are not *explicitly stated* in the text. If the text mentions "Fact A" and "Fact B" separately, you cannot create a question that implies a relationship "Fact C" unless that relationship is *also* explicitly stated.
        4.  **No Hallucination:** If a piece of information cannot be generated with 100% confidence from the text, you MUST omit it. If the source text is insufficient to generate the required number of questions, you MUST stop and output a simple JSON error message: "error": "Source text is insufficient to generate a high-quality quiz that meets all constraints."
        5.  **Schema Adherence:** You MUST adhere *perfectly* to the provided <JSON_SCHEMA>. The output MUST be a single, clean JSON object with no explanatory text, markdown, or commentary before or after it.
        </CORE_PRINCIPLES>

        <TASK_DEFINITION>
        You will receive a `<SOURCE_TEXT>`, an `<ARTICLE_TITLE>`, a `{difficulty}` ("Easy", "Medium", or "Hard"), and `<JSON_SCHEMA>`.
        Your task is to populate the <JSON_SCHEMA> based *only* on the `<SOURCE_TEXT>`.
        </TASK_DEFINITION>

        <MODULE_INSTRUCTIONS>

        ### 1. Summary Module (`summary`)
        - Generate a 2-3 sentence summary.
        - This summary MUST identify the central thesis, person, or event of the article.
        - It MUST state the *most significant attribute or accomplishment* as described in the text.
        - You MUST avoid generic definitions; focus on *what makes this topic notable* according to the text.

        ### 2. Sections Module (`main_sections`)
        - Extract the primary thematic section titles from the article.
        - You MUST *NEVER* include non-content, boilerplate sections (e.g., "See also", "References", "External links", "Contents", "Further reading").
        - If no thematic sections are present, output an empty list ``.

        ### 3. Entities Module (`key_entities`)
        - Scan the `<SOURCE_TEXT>` and extract the *most central and most repeated* named entities.
        - Limit the lists to a maximum of 7 entities per category.
        - All entities MUST be explicitly named in the text.
        - If no entities are found for a category, you MUST output an empty list ``.

        ### 4. Quiz Module (`questions` array)
        - You MUST generate *exactly 8* multiple-choice questions.
        - The difficulty distribution is NOT flexible and is determined by the {difficulty} input.

        ### 5. For each questions, add the related sections that are suggested to user to read to get more insights of this question.
        - Sections should directly related to the question.
        - Max of 1-3 sections.
        
        <DIFFICULTY_LOGIC>
        - **IF {difficulty} == "Easy":**
        - Generate **6 "Easy"** questions.
        - Generate **2 "Medium"** questions.
        - Generate **0 "Hard"** questions.
        - **IF {difficulty} == "Medium":**
        - Generate **2 "Easy"** questions.
        - Generate **5 "Medium"** questions.
        - Generate **1 "Hard"** question.
        - **IF {difficulty} == "Hard":**
        - Generate **1 "Easy"** question.
        - Generate **2 "Medium"** questions.
        - Generate **5 "Hard"** questions.
        </DIFFICULTY_LOGIC>

        <DIFFICULTY_DEFINITIONS>
        - **"Easy" (Factual Recall):** Tests *who, what, when, or where*. The answer is a single, discrete fact explicitly stated in the text.
        - **"Medium" (Contextual/Causal Reasoning):** Tests *how* or *why* something happened. The answer requires connecting 1-2 facts, typically from the same paragraph, to understand a process or a relationship.
        - **"Hard" (Analytical/Synthesis Reasoning):** Tests the *implications, consequences, or comparisons* described in the text. The answer requires synthesizing information from *multiple* sections or paragraphs to form a comprehensive conclusion.
        </DIFFICULTY_DEFINITIONS>

        <QUESTION_GENERATION_PROCESS>
        For *every single question*, you MUST follow this internal process:
        1.  **Find Quote:** First, identify a concise, verbatim `source_quote` from the `<SOURCE_TEXT>` that contains a meaningful fact.
        2.  **Formulate Question:** Write a question that tests understanding of that `source_quote`.
        3.  **Generate Answer:** The `correct_answer` MUST be 100% supported by the `source_quote`.
        4.  **Generate Distractors:** The `distractors` (incorrect options) MUST be plausible but *factually incorrect* according to the `<SOURCE_TEXT>`. *Never* invent information for distractors that is not related to the article's domain. If plausible distractors cannot be created from the text, find a new fact to test.
        5.  **Write Explanation:** The `explanation` MUST be a single, concise, declarative sentence.
            -   It MUST *only* contain the factual reason for the correct answer, based on the `source_quote`.
            -   It MUST *NEVER* use meta-references or preambles (e.g., "The article states...", "This is correct because...", "As per the text...").
            -   **Good Example:** "The event took place in 1955 as a protest against segregation."
            -   **Bad Example:** "As the article explains, the answer is 1955 because that is when the protest occurred."
        </QUESTION_GENERATION_PROCESS>

        </MODULE_INSTRUCTIONS>
    """
    )

    # Building the LangChain runnable chain
    chain: RunnableSequence = prompt | model | parser

    try:
        result = chain.invoke({
            "title": article_title,
            "content": relevant_text,
            "difficulty": difficulty
        })

        quiz_json = result.dict() if hasattr(result, "dict") else result.model_dump()
        return quiz_json

    except Exception as e:
        print(f"[Error] Quiz generation failed: {e}")
        return {"error": str(e), "title": article_title}


