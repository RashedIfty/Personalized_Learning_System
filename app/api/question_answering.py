import pickle
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.question_answering import QuestionRequest, AnswerResponse
from app.core.database import get_db
from app.db.crud.question_answering_crud import get_book_by_id, get_latest_book, log_query, get_query_history
from app.llm.question_answering_llm import generate_answer
from app.auth.auth import get_current_user  # Enforce authentication

qa_router = APIRouter()

@qa_router.post("/ask", response_model=AnswerResponse)
def ask_question(
    request: QuestionRequest, 
    db: Session = Depends(get_db), 
    book_id: int = Query(None, description="ID of the book to use"),
    current_user = Depends(get_current_user)  # Authentication required
):
    """Answer questions using a selected or the latest stored book for the current user."""
    
    # Retrieve the book scoped to the current user
    if book_id:
        book = get_book_by_id(db, book_id, user_id=current_user.id)
    else:
        book = get_latest_book(db, user_id=current_user.id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    # Generate answer using the LLM based on the book's text
    try:
        answer_text = generate_answer(book.text_content, request.question)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Log the query (recording the interaction in history)
    log_query(db, book.id, request.question, answer_text)

    return {"question": request.question, "answer": answer_text}


@qa_router.get("/history")
def get_query_history_endpoint(
    db: Session = Depends(get_db), 
    book_id: int = Query(None, description="Filter history by book ID"),
    current_user = Depends(get_current_user)  # Authentication required
):
    """Retrieve past queries and responses for the current user."""
    history = get_query_history(db, book_id, user_id=current_user.id)

    if not history:
        return {"message": "No query history found."}

    return [
        {
            "query": h.query, 
            "response": h.response, 
            "timestamp": h.created_at, 
            "book_id": h.book_id
        } for h in history
    ]
