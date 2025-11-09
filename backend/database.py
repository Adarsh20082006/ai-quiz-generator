from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime,Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/ai_quiz_db")  # Getting MySQL URL from .env

engine = create_engine(DATABASE_URL, echo=False)    # Creating DB engine

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Structure of DB table
class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    title = Column(String(255), nullable=False)
    date_generated = Column(DateTime, default=datetime.utcnow)
    scraped_content = Column(Text(length=4294967295), nullable=True)  # All scraped data will stored here
    full_quiz_data = Column(Text(length=4294967295), nullable=False)  # All Quiz contents stored here

def init_db():
    Base.metadata.create_all(bind=engine)   # Creating DB
    print("Database created!")


