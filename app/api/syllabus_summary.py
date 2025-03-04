import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.syllabus import SyllabusTopicsResponse, SyllabusSummaryRequest, SyllabusSummaryResponse
from app.core.database import get_db
from app.db.crud.syllabus_crud import save_syllabus_file, extract_syllabus_text, get_book_by_id, get_latest_book
from app.llm.syllabus_llm import extract_syllabus_topics, generate_syllabus_summary
from app.auth.auth import get_current_user

syllabus_router = APIRouter()

@syllabus_router.post("/upload_syllabus", response_model=SyllabusTopicsResponse)
def upload_syllabus_and_extract_topics(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """Upload a syllabus PDF and extract topics.
       If the same syllabus is uploaded again by the current user, reuse the existing file.
    """
    SYLLABUS_FOLDER = os.path.join("data", "syllabus")
    os.makedirs(SYLLABUS_FOLDER, exist_ok=True)
    
    # Create a unique filename for the current user
    unique_filename = f"{current_user.id}_{file.filename}"
    syllabus_path = os.path.join(SYLLABUS_FOLDER, unique_filename)
    
    # If the file already exists, reuse it
    if not os.path.exists(syllabus_path):
        try:
            syllabus_path = save_syllabus_file(file, unique_filename)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    try:
        syllabus_text = extract_syllabus_text(syllabus_path)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    try:
        topics = extract_syllabus_topics(syllabus_text)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"topics": topics}

@syllabus_router.post("/summarize", response_model=SyllabusSummaryResponse)
def summarize_syllabus(
    request: SyllabusSummaryRequest,
    db: Session = Depends(get_db),
    book_id: int = Query(None, description="ID of the book to use for summarization"),
    current_user = Depends(get_current_user)
):
    """Generate a summary for syllabus topics based on a selected book for the current user."""
    if not request.topics:
        raise HTTPException(status_code=400, detail="No topics provided for summarization.")
    
    # Retrieve the book for the current user
    if book_id:
        book = get_book_by_id(db, book_id, user_id=current_user.id)
    else:
        book = get_latest_book(db, user_id=current_user.id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    try:
        summaries = generate_syllabus_summary(book.text_content, request.topics, request.summary_type)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"summaries": summaries}
