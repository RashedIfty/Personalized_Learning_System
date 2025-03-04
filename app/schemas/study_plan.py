from pydantic import BaseModel


class StudyPlanRequest(BaseModel):
    duration: int

class StudyPlanResponse(BaseModel):
    study_plan: str