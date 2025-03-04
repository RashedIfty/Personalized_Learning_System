import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.llm.embeddings import create_embeddings
from app.db.crud.pdf_crud import (
    save_pdf_file,
    extract_text_from_pdf,
    save_embeddings_to_file,
    store_pdf_in_db,
    list_uploaded_books,
)
from app.models.book import Book
from app.auth.auth import get_current_user

pdf_router = APIRouter()

# Define central data storage paths
DATA_FOLDER = "data"
BOOKS_FOLDER = os.path.join(DATA_FOLDER, "books")
EMBEDDINGS_FOLDER = os.path.join(DATA_FOLDER, "embeddings")
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

# Ensure directories exist
os.makedirs(BOOKS_FOLDER, exist_ok=True)
os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)

@pdf_router.post("/upload_pdf")
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Upload and save a PDF file, then store embeddings in both SQLite and a file with a 200MB limit.
       The book is associated with the current user.
    """

    file_path = os.path.join(BOOKS_FOLDER, file.filename)
    embedding_path = os.path.join(EMBEDDINGS_FOLDER, f"{file.filename}.pkl")

    # Check file size before processing
    file.file.seek(0, os.SEEK_END)  # Move to end of file
    file_size = file.file.tell()  # Get file size in bytes
    file.file.seek(0)  # Reset cursor

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum allowed size is 200MB.")

    # Check if the book already exists for this user
    existing_book = db.query(Book).filter(
        Book.filename == file.filename,
        Book.user_id == current_user.id
    ).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="This book is already uploaded.")

    # Save the uploaded file in chunks (memory efficient)
    save_pdf_file(file, file_path)

    # Extract text safely
    text = extract_text_from_pdf(file_path)

    # Generate OpenAI embeddings (pass text as a string)
    embeddings = create_embeddings(text)

    # Save embeddings as a file
    save_embeddings_to_file(embedding_path, embeddings)

    # Store the book & embeddings in the database, associating with current user
    new_book = store_pdf_in_db(db, file.filename, text, embeddings, current_user.id)

    return {
        "message": "PDF uploaded and stored successfully!",
        "book_id": new_book.id,
        "embedding_file": embedding_path,
    }

@pdf_router.get("/list_books")
def list_books_endpoint(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all previously uploaded and embedded books for the current user."""
    return list_uploaded_books(db, current_user.id)
