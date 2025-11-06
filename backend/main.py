from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, HttpUrl
from scraper_service import get_or_create_scraped_data
from database import Base, engine

app=FastAPI()

# Create tables (only if not exist)
Base.metadata.create_all(bind=engine)

class BaseURL(BaseModel):
    url: HttpUrl 



@app.post('/')
def quiz(url:BaseURL):
    res=get_or_create_scraped_data(str(url.url))
    return res