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
    temperature=0.8
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
    You are an expert quiz generator. Create a JSON-formatted quiz based strictly on the given article.

    Instructions:
    - Carefully read the content.
    - Extract key points, sections, entities, and create high-quality MCQs based only on article content.
    - No hallucination. Avoid any external or uncertain facts.

    Output JSON Structure:
    - title: <article title>
    - summary: <concise summary>
    - key_entities:
        - people: ["List only names explicitly mentioned in the text. Include a maximum of 3, chosen by frequency of mention."]
        - organizations: ["List only organizations explicitly mentioned in the text. Include a maximum of 3, chosen by frequency of mention."]
        - locations: ["List only locations or country names explicitly present in the text. Include a maximum of 2."]
    -sections: ["List 3–5 concise domain-level themes or hash-tag-like keywords that represent the main areas covered in the article."]

    - quiz: list of questions with:
        - question: text
        - options: [A, B, C, D]
        - answer: correct option text
        - explanation: short reason (1 sentence max)
        - difficulty: easy | medium | hard
    - related_topics: 1-3 Wikipedia topics for further learning

    Difficulty Ratios (based on mode):
    - Easy mode → 70% easy, 20% medium, 10% hard
    - Medium mode → 25% easy, 60% medium, 15% hard
    - Hard mode → 10% easy, 30% medium, 60% hard

    Additional Requirements:
    - Questions must be diverse, accurate, and teaching-focused.
    - Extract the questions which are worth knowing answer to user.
    - Easy: Direct recall (what, when, who, where)
    - Medium: Slight reasoning or contextual
    - Hard: Indirect, deep, or surprising
    - Never include hallucinated or guessed facts.
    - Explanations must be short, useful, and non-confusing.
    - Avoid redundant or vague options.

    Article Title: {title}
    Article Content:
    {content}

    {format_instructions}
    """
    )


    chain = prompt | model | parser
    result = chain.invoke({"title": article_title, "content": relevant_text})
    result = chain.invoke({"title": article_title, "content": relevant_text})

# Convert Pydantic model → Python dict
    quiz_json = result.dict() if hasattr(result, "dict") else result.model_dump()

    return quiz_json


