from sqlalchemy.orm import Session
from app.models.book import Book

def get_book_by_id(db: Session, book_id: int, user_id: int = None):
    """Retrieve a book by ID, optionally filtering by user_id."""
    query = db.query(Book).filter(Book.id == book_id)
    if user_id is not None:
        query = query.filter(Book.user_id == user_id)
    return query.first()
