import os
import requests
from fastapi import APIRouter, HTTPException
from app.schemas.google_search import SearchRequest, SearchResponse, SearchResult
from app.core.config import settings

google_search_router = APIRouter()

SERPER_API_KEY = settings.SERPER_API_KEY
SERPER_API_URL = "https://google.serper.dev/search"

def search_google_serper(query: str, num_results: int = 10):
    """Fetch search results from Google using Serper API."""
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": num_results}

    response = requests.post(SERPER_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Error fetching search results: {response.text}")

    return response.json()

@google_search_router.post("/search", response_model=SearchResponse)
def fetch_search_results(request: SearchRequest):
    """Fetch Google search results using Serper API."""
    search_results = search_google_serper(request.query, request.num_results)

    results = []
    if "organic" in search_results:
        for result in search_results["organic"]:
            title = result.get("title", "No title available")
            snippet = result.get("snippet", "No description available")
            link = result.get("link", "#")
            source = result.get("source", "Unknown Source")

            # ✅ Filter out irrelevant results (like ads)
            if "ads" in link or "sponsored" in link:
                continue

            results.append(SearchResult(title=title, snippet=snippet, link=link, source=source))

    if not results:
        raise HTTPException(status_code=404, detail="No relevant search results found.")

    return {"results": results}
