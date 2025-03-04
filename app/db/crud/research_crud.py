from sqlalchemy.orm import Session
from app.models.book import Book
from app.db.crud.pdf_crud import extract_keywords

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

def extract_book_keywords(db: Session, book_id: int = None, user_id: int = None):
    """Extract keywords from a book for a specific user."""
    book = get_book_by_id(db, book_id, user_id=user_id) if book_id else get_latest_book(db, user_id=user_id)
    if not book:
        return None, "Book not found."

    keywords = extract_keywords(book.text_content)
    if not keywords:
        return None, "No keywords found in the book."

    return keywords, None