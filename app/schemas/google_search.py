from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    query: str
    num_results: int = 5

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str

class SearchResponse(BaseModel):
    results: List[SearchResult]