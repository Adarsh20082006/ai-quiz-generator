from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from scraper_service import get_or_create_scraped_data
from database import SessionLocal, Quiz, init_db
from llm_quiz_generator import generate_quiz
import json

# Initialize DB
init_db()

# FastAPI App
app = FastAPI(title="AI Wiki Quiz Generator")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Model to scrape the Wikipedia
class URLPreview(BaseModel):
    url: HttpUrl

# Model to request to generate the quiz
class QuizRequest(BaseModel):
    url: HttpUrl
    difficulty: str
    sections: list[str] | None = None


# Health route
@app.get("/")
def root():
    return {"message": "Backend is running and CORS is enabled!"}

# ...  POST/PUT routes below ...


@app.get("/debug")
def debug_env():
    import os
    return {
        "GOOGLE_API_KEY_SET": bool(os.getenv("GOOGLE_API_KEY")),
        "GEMINI_API_KEY_SET": bool(os.getenv("GEMINI_API_KEY"))
    }

@app.post("/generate_quiz",description='Getting data from wikipedia',tags=['Quiz']) #Srape and stores data in DB
async def preview_article(payload: URLPreview):
    try:
        scraped = get_or_create_scraped_data(str(payload.url))
        sections = [s["heading"] for s in scraped["sections"]]
        print(f"Got {scraped['title']}'s data!")
        return {"status":True,"title": scraped["title"], "available_sections": sections,"summary_points":scraped.get("summary_points", [])} # Returning {title, sections, summary_points}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/generate_quiz", description="Update quiz record with generated AI quiz", tags=["Quiz"])
async def generate_quiz_endpoint(payload: QuizRequest):
    db = SessionLocal()
    try:
        print(f"[REQUEST] Generating quiz for {payload.url} | Difficulty: {payload.difficulty}")

        existing = db.query(Quiz).filter(Quiz.url == str(payload.url)).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Scraped data not found. Please run /generate_quiz (POST) first.")

        scraped_data = json.loads(existing.scraped_content)
        print("[INFO] Scraped data loaded successfully.")

        quiz = generate_quiz(
            article_title=scraped_data["title"],
            structured_content=scraped_data,
            difficulty=payload.difficulty,
            selected_sections=payload.sections
        )

        if "error" in quiz:
            print(f"[LLM ERROR] {quiz['error']}")
            raise HTTPException(status_code=500, detail=quiz["error"])

        print("[INFO] Quiz generation successful.")
        existing.full_quiz_data = json.dumps(quiz, ensure_ascii=False)
        db.commit()

        return {"status": True, "quiz": quiz}

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        print(f"[EXCEPTION] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

    finally:
        db.close()



@app.get("/history", description='Getting the list of all saved quizzes.', tags=['Quiz']) # Getting all store records from DB
def get_history():
    db = SessionLocal()
    try:
        records = db.query(Quiz.id, Quiz.url, Quiz.title, Quiz.date_generated).all()
        history = [
            {
                "id": r.id,
                "url": r.url,
                "title": r.title,
                "date_generated": r.date_generated
            }
            for r in records
        ]
        return history  # Returning {id, url, title, date_generated}
    finally:
        db.close()

@app.get('/quiz/{quiz_id}',description="Getting the specific quiz based on the id", tags=['Quiz']) #For displaying each quiz using its id.
def get_quiz(quiz_id:int):
    db=SessionLocal()
    try:
        record = db.query(Quiz.id, Quiz.title, Quiz.full_quiz_data).filter(Quiz.id == quiz_id).first()

        if not record:
            raise HTTPException(status_code=404, detail="Quiz not found.")
        quiz_data = json.loads(record.full_quiz_data) # Deserialize JSON string into a Python dictionary
        return {'title':record.title,'quiz_data':quiz_data}
    finally:
        db.close()
