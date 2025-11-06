# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from scraper_service import get_or_create_scraped_data
from database import SessionLocal, Quiz, init_db
from llm_quiz_generator import generate_quiz
import json

init_db()
app = FastAPI(title="AI Wiki Quiz Generator")

class URLPreview(BaseModel):
    url: HttpUrl

class QuizRequest(BaseModel):
    url: HttpUrl
    difficulty: str
    sections: list[str] | None = None

@app.post("/get-data",description='Getting data from wikipedia',tags=['Quiz'])
def preview_article(payload: URLPreview):
    try:
        scraped = get_or_create_scraped_data(str(payload.url))
        sections = [s["heading"] for s in scraped["sections"]]
        print(f"Got {scraped['title']} data!")
        return {"title": scraped["title"], "available_sections": sections}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/quiz", description='Update quiz record with generated AI quiz', tags=['Quiz'])
def generate_quiz_endpoint(payload: QuizRequest):
    db = SessionLocal()
    try:
        # Fetch scraped content from DB (must exist already)
        existing = db.query(Quiz).filter(Quiz.url == str(payload.url)).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Scraped data not found. Please run /get-data first.")

        scraped_data = json.loads(existing.scraped_content)

        # Generate quiz using the already scraped content
        quiz_json = generate_quiz(
            article_title=scraped_data["title"],
            structured_content=scraped_data,
            difficulty=payload.difficulty,
            selected_sections=payload.sections
        )

        # Update DB with quiz data
        existing.full_quiz_data = json.dumps(quiz_json, ensure_ascii=False)
        db.commit()
        db.refresh(existing)

        print(f"Quiz generated and stored for '{scraped_data['title']}'")
        return quiz_json

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")
    finally:
        db.close()
