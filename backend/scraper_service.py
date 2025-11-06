# scraper_service.py
import json
from fastapi import HTTPException
from database import SessionLocal, Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz
from datetime import datetime

def get_or_create_scraped_data(url: str, difficulty="Medium", selected_sections=None):
    db = SessionLocal()
    try:
        existing = db.query(Quiz).filter(Quiz.url == url).first()
        if existing:
            print("Cache hit! — returning stored quiz")
            return json.loads(existing.full_quiz_data)

        scraped_data = scrape_wikipedia(url)
        quiz_output = generate_quiz(scraped_data["title"], scraped_data, difficulty, selected_sections)
        quiz_json = quiz_output.dict()
        new_entry = Quiz(
            url=url,
            title=scraped_data["title"],
            date_generated=datetime.utcnow(),
            scraped_content=json.dumps(scraped_data, ensure_ascii=False),
            full_quiz_data=json.dumps(quiz_json, ensure_ascii=False)
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        quiz_json["id"] = new_entry.id
        print(f"✅ Stored quiz for '{scraped_data['title']}'")
        return quiz_json

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        db.close()
