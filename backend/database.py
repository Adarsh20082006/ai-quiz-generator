from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime,Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use environment variable for DB connection
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/ai_quiz_db")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session for DB operations
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Declarative Base
Base = declarative_base()


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    title = Column(String(255), nullable=False)
    date_generated = Column(DateTime, default=datetime.utcnow)
    scraped_content = Column(JSON, nullable=True)
    full_quiz_data = Column(Text, nullable=False)


