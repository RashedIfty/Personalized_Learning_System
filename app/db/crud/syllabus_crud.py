import os
from sqlalchemy.orm import Session
from app.models.book import Book
from app.api.pdf_processing import extract_text_from_pdf

DATA_FOLDER = "data"
SYLLABUS_FOLDER = os.path.join(DATA_FOLDER, "syllabus")
os.makedirs(SYLLABUS_FOLDER, exist_ok=True)

def save_syllabus_file(file, filename: str = None):
    """Save uploaded syllabus file.
       If a custom filename is provided, use it; otherwise use the file's original name.
    """
    if filename is None:
        filename = file.filename
    syllabus_path = os.path.join(SYLLABUS_FOLDER, filename)
    try:
        with open(syllabus_path, "wb") as f:
            f.write(file.file.read())
        return syllabus_path
    except Exception as e:
        raise RuntimeError(f"Error saving file: {str(e)}")

def extract_syllabus_text(file_path):
    """Extract text from syllabus PDF."""
    try:
        syllabus_text = extract_text_from_pdf(file_path)
        if not syllabus_text.strip():
            raise RuntimeError("Failed to extract text from syllabus. The file may be empty or non-text-based.")
        return syllabus_text
    except Exception as e:
        raise RuntimeError(f"Error extracting text: {str(e)}")

# Optionally update the book-retrieval functions to enforce per-user filtering
def get_book_by_id(db: Session, book_id: int, user_id: int = None):
    """Retrieve a book by its ID, optionally filtering by user_id."""
    query = db.query(Book).filter(Book.id == book_id)
    if user_id is not None:
        query = query.filter(Book.user_id == user_id)
    return query.first()

def get_latest_book(db: Session, user_id: int = None):
    """Retrieve the most recently uploaded book, optionally filtering by user_id."""
    query = db.query(Book)
    if user_id is not None:
        query = query.filter(Book.user_id == user_id)
    return query.order_by(Book.uploaded_at.desc()).first()
