import requests
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.research import ResearchRequest, ResearchResponse, ResearchPaper, KeywordResponse
from app.core.database import get_db
from app.db.crud.research_crud import get_book_by_id, get_latest_book
from app.llm.research_llm import extract_keywords_from_text
from app.auth.auth import get_current_user  # Enforce authentication

research_router = APIRouter()

CROSSREF_API_URL = "https://api.crossref.org/works"

@research_router.get("/keywords", response_model=KeywordResponse)
def get_book_keywords(
    db: Session = Depends(get_db),
    book_id: int = None,
    current_user = Depends(get_current_user)
):
    """Extract keywords from a selected book for the current user."""
    if book_id:
        book = get_book_by_id(db, book_id, user_id=current_user.id)
    else:
        book = get_latest_book(db, user_id=current_user.id)
        
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    try:
        keywords = extract_keywords_from_text(book.text_content)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"keywords": keywords}

@research_router.post("/search", response_model=ResearchResponse)
def fetch_research_papers(
    request: ResearchRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Fetch research papers based on a user query or, if no query is provided,
       extract keywords from the latest book uploaded by the current user.
    """
    # If no query provided, fetch the latest book for the current user and use its keywords
    if not request.query:
        book = get_latest_book(db, user_id=current_user.id)
        if not book:
            raise HTTPException(status_code=400, detail="No book uploaded yet for the current user.")
        try:
            keywords = extract_keywords_from_text(book.text_content)
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))
        if not keywords:
            raise HTTPException(status_code=400, detail="No keywords found in the book.")
        request.query = keywords[0]  # Use the first keyword as the default query

    # Prepare parameters for the Crossref API
    params = {"query": request.query, "rows": request.num_papers}
    response = requests.get(CROSSREF_API_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching research papers.")

    data = response.json()
    papers = []

    for item in data.get("message", {}).get("items", []):
        papers.append(
            ResearchPaper(
                title=item.get("title", ["No title available"])[0],
                link=item.get("URL", ""),
                abstract=item.get("abstract", "Abstract not available"),
                authors=[
                    f"{author.get('family', '')}, {author.get('given', '')}"
                    for author in item.get("author", [])
                    if "family" in author and "given" in author
                ]
            )
        )

    if not papers:
        raise HTTPException(status_code=404, detail="No research papers found for the given query.")

    return {"query": request.query, "papers": papers}
