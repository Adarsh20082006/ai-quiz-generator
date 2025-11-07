# llm_quiz_generator.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import QuizOutput
from vector_service import build_faiss_index

load_dotenv()
parser = PydanticOutputParser(pydantic_object=QuizOutput)
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.5
)

def generate_quiz(article_title: str, structured_content: dict, difficulty="Medium", selected_sections=None):
    sections = structured_content.get("sections", [])
    if selected_sections:
        sections = [s for s in sections if s["heading"] in selected_sections ]

    article_text = "\n".join(
        (s.get("content", "")) + " " + " ".join(sub.get("content", "") for sub in s.get("subsections", []))
        for s in sections
    )

    vector_store, _ = build_faiss_index(article_text)
    query = f"important facts, achievements, and insights about {article_title}"
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 10})
    docs = retriever.invoke(query)  # Correct method for LangChain v0.3+

    relevant_text = "\n".join([d.page_content for d in docs])

    prompt = PromptTemplate(
        input_variables=["title", "content"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
        template="""   
        You are an expert educational quiz generator. Your goal is to create a JSON-formatted quiz strictly based on the given Wikipedia article content — ensuring factual accuracy, coverage diversity, and teaching effectiveness.

        'Article Title:' {title}  
        'Article Content:' 
        {content}  

        {format_instructions}

        Follow all the instructions carefully.

        Primary Objectives:
        - Transform the article into a 'rich, structured quiz dataset'.
        - Ensure every question, summary point, and entity is 'fully grounded in the provided text'.
        - Never include hallucinated, assumed, or guessed information.
        - Maintain educational value by making each question teach something meaningful.

        Additional Rules & Guidelines

        Question Generation:
        - Create '8 questions' from the article.
        - Ensure a 'good balance' of direct recall and reasoning questions.
        - Each question should test 'understanding' — not just memory.
        - Avoid repeating similar facts or rephrasing existing questions.

        Difficulty Distribution:
        Use these ratios for each mode:
        - Easy mode → 70% easy, 20% medium, 10% hard  
        - Medium mode → 25% easy, 60% medium, 15% hard  
        - Hard mode → 10% easy, 30% medium, 60% hard  

        > “Easy” = direct factual (who/what/when/where)  
        > “Medium” = contextual (why/how/simple reasoning)  
        > “Hard” = analytical, indirect, or critical facts.

        Explanation Rules:
        - Each explanation should be concise and crisp.
        - Should clarify why the answer is correct.
        - Avoid vague wording like “as per the article” — don't specific like this, Just give response by considering all the data is valid.

        Summary Rules:
        - The summary should not be generic — it should feel **tailored** to the topic.

        Key Entity Extraction:
        - Extract only 'explicit mentions' — not inferred connections.
        - Prioritize the most 'frequently mentioned' entities.
        - Don’t mix people with organizations or locations.

        Section Listing:
        - Use short, thematic section names (like “Career Beginnings”, “Major Works”, “Awards”).
        - Skip boilerplate sections like “See also”, “References”, “External links”.

        Accuracy Guidelines:
        - If uncertain about a detail, skip it entirely.
        - Never invent options or add extra entities beyond the article text.
        - Ensure clean JSON format — no Markdown or commentary.

        Final Note:
        Be 'factually strict', 'educationally creative', and 'JSON-accurate'.  
        Focus on 'teaching through questioning', not tricking the learner.  
        Avoid speculative, unrelated, or vague information.
    """
    )


    chain = prompt | model | parser
    result = chain.invoke({"title": article_title, "content": relevant_text})
    result = chain.invoke({"title": article_title, "content": relevant_text})

# Convert Pydantic model → Python dict
    quiz_json = result.dict() if hasattr(result, "dict") else result.model_dump()

    return quiz_json


