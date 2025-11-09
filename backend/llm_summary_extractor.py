# llm_summary_extractor.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv() # Loading API keys from .env
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
# Initialize model (fast and stable)
summary_model = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-lite",  # For Fast & efficient summaries
    google_api_key=api_key,
    temperature=0.25,
)

# Define structured summarization prompt
summary_prompt = PromptTemplate.from_template("""
You are an expert summarizer and educator.
Read the following article carefully and extract **10 concise, factual, and insightful key summary points** and return as a JSON list of strings.

Guidelines:
- Do NOT repeat trivial info already in the title.
- Include only specific, verified, and educational facts that would help a learner understand the article.
- Avoid vague or repetitive statements.
- Write each point as a short and clear sentence.
- Skip any uncertain or unverified information.
Example:
[
  "Alan Turing developed the concept of the Turing Machine, forming the basis of modern computing.",
  "During World War II, he led codebreaking efforts at Bletchley Park."
]
Article Title: {title}
Article Content:
{content}
""")

import json
import re

def generate_summary_points(title: str, content: str):
    """Generate 10 key factual summaries."""
    chain = summary_prompt | summary_model
    response = chain.invoke({"title": title, "content": content})
    text = response.content.strip()

    # Remove markdown wrappers like ```json ... ```
    text = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()

    # Try parsing clean JSON
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
    except Exception as e:
        print(f"[Error] Summary generation failed: {e}")
        return ["Could not generate summary at this time."]

    # Fallback: Extract lines manually
    lines = [line.strip(" -•\"\',") for line in text.splitlines() if line.strip()]
    return [l for l in lines if len(l) > 5][:]

    
