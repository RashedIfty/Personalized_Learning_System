import os
import glob
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.answer_key import AnswerKeyResponse
from app.api.pdf_processing import extract_text_from_pdf
from app.core.database import get_db
from app.db.crud.answer_key_crud import save_question_paper, get_book_by_id
from app.llm.answer_key_llm import generate_answers_from_book
from app.auth.auth import get_current_user  # Enforce authentication

answer_key_router = APIRouter()

@answer_key_router.post("/upload_question_paper")
def upload_question_paper(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """Upload a question paper PDF and store it.
       If the same paper is uploaded again for the same user, reuse the existing file.
    """
    QUESTIONS_FOLDER = os.path.join("data", "questions")
    os.makedirs(QUESTIONS_FOLDER, exist_ok=True)
    
    # Create a unique filename for this user (prefix with user ID)
    unique_filename = f"{current_user.id}_{file.filename}"
    qp_path = os.path.join(QUESTIONS_FOLDER, unique_filename)
    
    # If the file already exists, return its info without re-saving it
    if os.path.exists(qp_path):
        return {"message": "Question paper already uploaded!", "filename": unique_filename}
    
    try:
        qp_path = save_question_paper(file, unique_filename)
        return {"message": "Question paper uploaded successfully!", "filename": unique_filename}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@answer_key_router.post("/generate_answers", response_model=AnswerKeyResponse)
def generate_answer_key(
    book_id: int = Query(..., description="ID of the book to use for generating answers"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generate answers for questions extracted from the current user's uploaded question paper PDF,
       using the book's content as context for generating the answers.
    """
    # Retrieve the book for the current user
    book = get_book_by_id(db, book_id, user_id=current_user.id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    # Automatically determine the current user's question paper file
    QUESTIONS_FOLDER = os.path.join("data", "questions")
    pattern = os.path.join(QUESTIONS_FOLDER, f"{current_user.id}_*")
    matching_files = glob.glob(pattern)
    if not matching_files:
        raise HTTPException(status_code=404, detail="No question paper found for the current user.")
    # Select the most recently modified question paper file
    qp_path = max(matching_files, key=os.path.getmtime)
    
    # Extract text from the question paper PDF and split into individual questions
    try:
        qp_text = extract_text_from_pdf(qp_path)
        extracted_questions = [q.strip() for q in qp_text.split("\n") if q.strip()]
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Error processing question paper: {str(e)}")
    
    if not extracted_questions:
        raise HTTPException(status_code=400, detail="No questions found in the question paper.")
    
    # Generate answers using the book's text as context for each extracted question
    try:
        answers = generate_answers_from_book(book.text_content, extracted_questions)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"answers": answers}
