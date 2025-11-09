# scraper_service.py
import json
from fastapi import HTTPException
from database import SessionLocal, Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz
from llm_summary_extractor import generate_summary_points
from datetime import datetime


def get_or_create_scraped_data(url: str):
    db = SessionLocal()
    try:
        existing = db.query(Quiz).filter(Quiz.url == url).first() # Checking the data in DB(Cache)
        if existing:
            print("Cache hit – returning stored data")
            scraped_data = json.loads(existing.scraped_content)
            # Return with summary points if available
            return {**scraped_data, "summary_points": scraped_data.get("summary_points", [])} # Returning {All scraped data, summary_points}

        # Scrape new article
        scraped_data = scrape_wikipedia(url)
        formatted_content = json.dumps(scraped_data, ensure_ascii=False)

        # Generate summary points for user revision
        summary_points = generate_summary_points(scraped_data["title"], " ".join(
            [s["content"] for s in scraped_data["sections"][:5]]
        ))

        # Add to scraped data
        scraped_data["summary_points"] = summary_points

        # Save in DB
        new_entry = Quiz(
            url=url,
            title=scraped_data["title"],
            scraped_content=json.dumps(scraped_data, ensure_ascii=False),
            full_quiz_data=json.dumps({}, ensure_ascii=False)
        )
        db.add(new_entry)   # Adding and updating the DB
        db.commit()
        db.refresh(new_entry)

        print("New data scraped and stored!")
        return scraped_data

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving scraped data: {str(e)}")
    finally:
        db.close()






