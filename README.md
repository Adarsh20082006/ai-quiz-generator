# 🧠 AI Quiz Generator

A full-stack AI-powered application that scrapes Wikipedia articles and generates structured, multi-level quizzes using Google Gemini API. Built with FastAPI (backend), React + TailwindCSS (frontend), and MySQL (DB), all containerized with Docker.

---

## 📦 Tech Stack

- **Frontend:** React 19 + Vite + TailwindCSS
- **Backend:** FastAPI + LangChain + Gemini (Google Generative AI)
- **Database:** MySQL 8 (Dockerized)
- **AI Model:** Gemini 2.5 Flash via LangChain
- **Vector Search:** FAISS for semantic relevance
- **Containerization:** Docker & Docker Compose

---

## 🚀 Getting Started

### 1. Clone and Set Up
```bash
git clone https://github.com/yourusername/ai-quiz-generator.git
cd ai-quiz-generator


2. Configure Environment

Create a .env file in backend/:

GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=mysql+pymysql://root:your_password@db:3306/ai_quiz_db


Replace your_gemini_api_key with your Google Gemini API key.

🐳 Running the Project

Build and run all services:

docker-compose up --build


Wait for containers (frontend, backend, and db) to be healthy. Access at:

Frontend: http://localhost:5173

Backend: http://localhost:8000/docs
 (Swagger UI)

MySQL: localhost:3310 (root / your password)

🔗 API Endpoints (FastAPI)
Method	Endpoint	Description
GET	/health	Check service health
POST	/scrape	Scrapes article from Wikipedia
POST	/quiz/generate	Generates quiz using Gemini
GET	/quiz/{title}	Fetches quiz for a specific article
GET	/quizzes	Returns all quizzes stored
🔄 App Flow
➤ 1. Input Wikipedia Topic

User enters a topic like Marie Curie.

➤ 2. Backend Scrapes Article

FastAPI service fetches and parses structured content from Wikipedia.

➤ 3. FAISS + Gemini Generation

FAISS builds a vector index of the text.

Top relevant chunks are fed to Gemini with strict grounding and schema.

Gemini returns a JSON containing:

Summary

Sections

Key Entities

8 MCQs (Easy, Medium, Hard)

➤ 4. Database Storage

Quiz is stored in MySQL (if not already present).

➤ 5. Frontend Display

React app displays summary + quiz in a user-friendly interface.

🧪 Development Tips

To run just the backend:

docker-compose run backend


Run frontend with live reload:

cd frontend && npm install && npm run dev

⚙️ Docker Configuration Summary
Ports
Service	Internal	Host
Frontend	5173	5173
Backend	8000	8000
MySQL	3306	3310
Services

db: MySQL with volume db_data

backend: FastAPI service

frontend: React app served by Vite

📂 Project Structure
.
├── backend
│   ├── main.py
│   ├── database.py
│   ├── scraper_service.py
│   ├── llm_quiz_generator.py
│   └── models.py
├── frontend
│   ├── src/
│   ├── vite.config.js
│   └── ...
├── docker-compose.yml
└── README.md

❓ Troubleshooting

Frontend not loading? Check Vite runs on 0.0.0.0 inside Docker or adjust Dockerfile.

CORS error? Confirm CORS is allowed in FastAPI and VITE_API_BASE_URL points to http://localhost:8000.

DB errors? Ensure MySQL is using port 3310:3306 and DATABASE_URL references db, not localhost.