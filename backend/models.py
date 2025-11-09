# models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# Used in QuizOutput to store key_entities
class KeyEntities(BaseModel):
    people: Optional[List[str]] = []
    organizations: Optional[List[str]] = []
    locations: Optional[List[str]] = []

# Used in QuizOutput to store quiz
class Question(BaseModel):
    question: str = Field(..., description="Quiz question text")
    options: List[str] = Field(..., description="List of 4 options")
    answer: str = Field(..., description="Correct answer")
    difficulty: str = Field(..., description="Difficulty: easy, medium, or hard")
    explanation: Optional[str] = Field(None, description="Explanation for answer")
    section: Optional[str] = Field(None, description="Section this question is based on")

# The QuizOutput structure 
class QuizOutput(BaseModel):
    id: Optional[int] = Field(None, description="DB primary key")
    url: str = Field(..., description="Wikipedia article URL")
    title: str = Field(..., description="Article title")
    summary: str = Field(..., description="Article summary")    # Contains the summary points
    key_entities: Optional[KeyEntities] = None  # Contains people, organisations, locations fields
    sections: List[str] = Field(..., description="Main section titles")
    quiz: List[Question] = Field(..., description="List of quiz questions") # Contains all ques and ans
    related_topics: Optional[List[str]] = []
