from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.study_plan import StudyPlanRequest, StudyPlanResponse
from app.core.database import get_db
from app.db.crud.study_plan_crud import get_book_by_id
from app.llm.study_plan_llm import generate_study_plan_from_text
from app.auth.auth import get_current_user  # Enforce authentication

study_router = APIRouter()

@study_router.post("/generate", response_model=StudyPlanResponse)
def generate_study_plan(
    request: StudyPlanRequest, 
    book_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # Authentication required
):
    """Generate a study plan from a stored book for the current user."""
    
    # Retrieve the book scoped to the current user
    book = get_book_by_id(db, book_id, user_id=current_user.id)
    if not book:
        raise HTTPException(status_code=400, detail="Book not found.")

    # Generate the study plan using the book's text and the provided duration
    try:
        study_plan = generate_study_plan_from_text(book.text_content, request.duration)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"study_plan": study_plan}
