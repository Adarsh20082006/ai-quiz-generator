import json
from fastapi import HTTPException
from database import SessionLocal, Quiz
from scraper import scrape_wikipedia
from datetime import datetime


def get_or_create_scraped_data(url: str):
    db = SessionLocal()
    try:
        # 🔹 1. Check cache
        existing_quiz = db.query(Quiz).filter(Quiz.url == url).first()
        if existing_quiz:
            print("✅ Cache hit — returning stored data")
            # Deserialize text to dict
            return json.loads(existing_quiz.scraped_content)

        # 🔹 2. Scrape fresh data
        scraped_data = scrape_wikipedia(url)
        structured_json = json.dumps(scraped_data, ensure_ascii=False)

        # 🔹 3. Save as text (stringified JSON)
        new_quiz = Quiz(
            url=url,
            title=scraped_data["title"],
            date_generated=datetime.utcnow(),
            scraped_content=structured_json,  # Text field
            full_quiz_data="{}"  # empty placeholder
        )
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)

        print(f"✅ Scraped and stored structured data for '{scraped_data['title']}'")
        return scraped_data

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving scraped data: {str(e)}")
    finally:
        db.close()
