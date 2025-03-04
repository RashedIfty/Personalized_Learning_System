from pydantic import BaseModel
from typing import List, Optional

class KeywordResponse(BaseModel):
    keywords: List[str]

class ResearchRequest(BaseModel):
    query: Optional[str] = None
    num_papers: int = 5

class ResearchPaper(BaseModel):
    title: str
    link: str
    abstract: str
    authors: List[str]

class ResearchResponse(BaseModel):
    query: str
    papers: List[ResearchPaper]
