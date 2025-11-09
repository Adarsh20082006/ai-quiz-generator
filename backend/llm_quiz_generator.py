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
    You are an expert Educational Content Designer and meticulous Fact-Checker.
    Your sole goal is to transform the given Wikipedia article content into a **structured, factual, and complete JSON quiz**.

    <ARTICLE_TITLE>
    {title}
    </ARTICLE_TITLE>

    <SOURCE_TEXT>
    {content}
    </SOURCE_TEXT>

    <JSON_SCHEMA>
    {format_instructions}
    </JSON_SCHEMA>

    <CONFIG>
    Difficulty Mode: {difficulty}
    </CONFIG>

    <CORE_RULES>
    1. **Zero Hallucination:** You must only use facts explicitly stated in <SOURCE_TEXT>.
    2. **No Missing Fields:** Every field from <JSON_SCHEMA> must exist and be filled — never leave null, empty lists, or blank values.
    3. **Fallback Policy:** 
       - If data for a field (like sections, key_entities, or explanations) is missing, fill it meaningfully with "N/A" or a short placeholder sentence. 
       - Example: instead of `null` or `[]`, write `"N/A"` or `["N/A"]`.
    4. **No Extra Output:** Return a **single, valid JSON object only** — no commentary, no markdown, no text outside JSON.
    5. **Content Authenticity:** Every quiz question, answer, and explanation must directly originate from the <SOURCE_TEXT>.
    6. **Completeness Requirement:** Ensure at least one entry exists in every array field (`key_entities`, `sections`, `quiz`, etc.).
    </CORE_RULES>

    <TASK_DESCRIPTION>
    Based on the provided <SOURCE_TEXT> and <ARTICLE_TITLE>, generate a factual quiz that matches the <JSON_SCHEMA>.
    Your response will include:
    - A 2–3 line summary.
    - Thematic sections (omit boilerplate like "See also", "References").
    - Key entities: people, organizations, and locations.
    - Exactly 8 multiple-choice questions (MCQs) following the difficulty configuration below.
    </TASK_DESCRIPTION>

    <DIFFICULTY_DISTRIBUTION>
    - If {difficulty} == "Easy": 6 Easy, 2 Medium
    - If {difficulty} == "Medium": 2 Easy, 5 Medium, 1 Hard
    - If {difficulty} == "Hard": 1 Easy, 2 Medium, 5 Hard
    </DIFFICULTY_DISTRIBUTION>

    <QUESTION_GUIDELINES>
    For each MCQ:
    - **Question:** Derived directly from a specific fact or statement.
    - **Options:** 4 total (1 correct + 3 distractors).
    - **Answer:** One correct factual answer.
    - **Difficulty:** easy, medium, or hard (as per config).
    - **Explanation:** One factual sentence supporting the answer.
    - **Section:** Add the relevant section name or "General".
    </QUESTION_GUIDELINES>
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
    <OUTPUT_CONSTRAINTS>
    - Return all required JSON fields, even if approximate.
    - Do not return empty arrays, missing keys, or null values.
    - Do not prefix or suffix your output with commentary, code blocks, or markdown.
    </OUTPUT_CONSTRAINTS>
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


