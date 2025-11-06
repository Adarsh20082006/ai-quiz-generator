# scraper_service.py
import json
from fastapi import HTTPException
from database import SessionLocal, Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz
from datetime import datetime

def get_or_create_scraped_data(url: str):
    db = SessionLocal()
    try:
        existing = db.query(Quiz).filter(Quiz.url == url).first()
        if existing:
            print("Cache hit! using stored scraped content.")
            return json.loads(existing.scraped_content)

        # Otherwise, scrape and cache
        scraped_data = scrape_wikipedia(url)
        structured_json = json.dumps(scraped_data, ensure_ascii=False)

        new_entry = Quiz(
            url=url,
            title=scraped_data["title"],
            date_generated=datetime.utcnow(),
            scraped_content=structured_json,
            full_quiz_data=json.dumps({}, ensure_ascii=False)  # placeholder
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        print(f"Scraped new data of {scraped_data["title"]} and stored successfully.")
        return scraped_data

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving scraped data: {str(e)}")
    finally:
        db.close()