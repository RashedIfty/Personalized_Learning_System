from pydantic import BaseModel
from typing import List

class QuizRequest(BaseModel):
    num_questions: int

class QuizResponse(BaseModel):
    quiz_questions: List[str]

