# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from scraper_service import get_or_create_scraped_data
from scraper import scrape_wikipedia
from database import init_db

init_db()
app = FastAPI(title="AI Wiki Quiz Generator")

class URLPreview(BaseModel):
    url: HttpUrl

class QuizRequest(BaseModel):
    url: HttpUrl
    difficulty: str
    sections: list[str] | None = None

@app.post("/preview")
def preview_article(payload: URLPreview):
    """Preview article title and available sections before generation."""
    try:
        scraped = scrape_wikipedia(str(payload.url))
        sections = [s["heading"] for s in scraped["sections"]]
        return {"title": scraped["title"], "available_sections": sections}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_quiz")
def generate_quiz_endpoint(payload: QuizRequest):
    """Generate and store quiz based on difficulty and selected sections."""
    try:
        quiz_data = get_or_create_scraped_data(str(payload.url), payload.difficulty, payload.sections)
        return quiz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
