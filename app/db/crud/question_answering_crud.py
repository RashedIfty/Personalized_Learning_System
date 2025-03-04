# app/db/crud/question_answering_crud.py

from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.history import QueryHistory

def get_book_by_id(db: Session, book_id: int, user_id: int = None):
    """Retrieve a book by ID, optionally filtering by user_id."""
    query = db.query(Book).filter(Book.id == book_id)
    if user_id is not None:
        query = query.filter(Book.user_id == user_id)
    return query.first()

def get_latest_book(db: Session, user_id: int = None):
    """Retrieve the most recently uploaded book, optionally for a specific user."""
    query = db.query(Book)
    if user_id is not None:
        query = query.filter(Book.user_id == user_id)
    return query.order_by(Book.uploaded_at.desc()).first()

def log_query(db: Session, book_id: int, query_text: str, response: str):
    """Log a user query and response in the database."""
    new_query = QueryHistory(book_id=book_id, query=query_text, response=response)
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

def get_query_history(db: Session, book_id: int = None, user_id: int = None):
    """Retrieve past queries and responses from history, optionally filtering by user."""
    q = db.query(QueryHistory)
    if book_id:
        q = q.filter(QueryHistory.book_id == book_id)
    if user_id:
        # Join with Book table to filter by Book.user_id
        q = q.join(Book).filter(Book.user_id == user_id)
    return q.order_by(QueryHistory.created_at.desc()).all()
