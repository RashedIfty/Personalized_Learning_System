from fastapi import FastAPI
from app.api.auth_endpoints import router as auth_router
from app.api.answer_key_generation import answer_key_router
from app.api.google_search import google_search_router
from app.api.pdf_processing import pdf_router
from app.api.question_answering import qa_router
from app.api.quiz_generation import quiz_router
from app.api.research_papers import research_router
from app.api.study_plan import study_router
from app.api.syllabus_summary import syllabus_router
from app.core.database import init_db

app = FastAPI(title="Personalized Learning System")
init_db()

# Include authentication endpoints (register & login)
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

# Include other endpoints (protected endpoints require authentication)
app.include_router(pdf_router, prefix="/api/pdf", tags=["PDF Upload"])
app.include_router(qa_router, prefix="/api/qa", tags=["Question Answering"])
app.include_router(quiz_router, prefix="/api/quiz", tags=["Quiz Generation"])
app.include_router(answer_key_router, prefix="/api/answer_key", tags=["Answer Key"])
app.include_router(syllabus_router, prefix="/api/syllabus", tags=["Syllabus Summary"])
app.include_router(research_router, prefix="/api/research", tags=["Research Papers"])
app.include_router(study_router, prefix="/api/study_plan", tags=["Study Plan"])

# Google search remains public
app.include_router(google_search_router, prefix="/api/search", tags=["Google Search"])

@app.get("/")
def home():
    return {"message": "Welcome to Personalized Learning System"}