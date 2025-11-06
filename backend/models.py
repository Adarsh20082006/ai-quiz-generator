# models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class KeyEntities(BaseModel):
    people: Optional[List[str]] = []
    organizations: Optional[List[str]] = []
    locations: Optional[List[str]] = []

class Question(BaseModel):
    question: str = Field(..., description="Quiz question text")
    options: List[str] = Field(..., description="List of 4 options")
    answer: str = Field(..., description="Correct answer")
    difficulty: str = Field(..., description="Difficulty: easy, medium, or hard")
    explanation: Optional[str] = Field(None, description="Explanation for answer")
    section: Optional[str] = Field(None, description="Section this question is based on")

class QuizOutput(BaseModel):
    id: Optional[int] = Field(None, description="DB primary key")
    url: str = Field(..., description="Wikipedia article URL")
    title: str = Field(..., description="Article title")
    summary: str = Field(..., description="Article summary")
    key_entities: Optional[KeyEntities] = None
    sections: List[str] = Field(..., description="Main section titles")
    quiz: List[Question] = Field(..., description="List of quiz questions")
    related_topics: Optional[List[str]] = []
