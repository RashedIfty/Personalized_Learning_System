from pydantic import BaseModel
from typing import List

class SyllabusTopicsResponse(BaseModel):
    topics: List[str]

class SyllabusSummaryRequest(BaseModel):
    topics: List[str]
    summary_type: str  # 'short' or 'detailed'

class SyllabusSummaryResponse(BaseModel):
    summaries: List[dict]  # {'topic': ..., 'summary': ...}
