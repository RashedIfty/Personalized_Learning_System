from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.quiz import QuizRequest, QuizResponse
from app.core.database import get_db
from app.db.crud.quiz_crud import get_book_by_id
from app.llm.quiz_llm import generate_quiz_questions
from app.auth.auth import get_current_user  # Enforce authentication

quiz_router = APIRouter()

@quiz_router.post("/generate", response_model=QuizResponse)
def generate_quiz(
    request: QuizRequest, 
    book_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # Authentication required
):
    """Generate quiz questions and answers from a previously uploaded book for the current user."""
    
    # Retrieve the book scoped to the current user
    book = get_book_by_id(db, book_id, user_id=current_user.id)
    if not book:
        raise HTTPException(status_code=400, detail="Book not found.")

    # Generate quiz using LLM
    try:
        quiz_questions = generate_quiz_questions(book.text_content, request.num_questions)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"quiz_questions": quiz_questions}
