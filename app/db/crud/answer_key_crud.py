import os
from sqlalchemy.orm import Session
from app.models.book import Book

DATA_FOLDER = "data"
QUESTION_PAPER_FOLDER = os.path.join(DATA_FOLDER, "questions")

# Ensure the folder exists
os.makedirs(QUESTION_PAPER_FOLDER, exist_ok=True)

def save_question_paper(file, filename: str = None):
    """Save uploaded question paper to the local directory.
       If a custom filename is provided, use it; otherwise use the file's original name.
    """
    if filename is None:
        filename = file.filename
    qp_path = os.path.join(QUESTION_PAPER_FOLDER, filename)
    try:
        with open(qp_path, "wb") as f:
            f.write(file.file.read())
        return qp_path
    except Exception as e:
        raise RuntimeError(f"Error saving file: {str(e)}")

def get_book_by_id(db: Session, book_id: int, user_id: int = None):
    """Retrieve a book by ID, optionally filtering by user_id."""
    query = db.query(Book).filter(Book.id == book_id)
    if user_id is not None:
        query = query.filter(Book.user_id == user_id)
    return query.first()
