from pydantic import BaseModel
from typing import List

class AnswerKeyResponse(BaseModel):
    answers: List[dict]  # Each item contains {'question': ..., 'answer': ...}
