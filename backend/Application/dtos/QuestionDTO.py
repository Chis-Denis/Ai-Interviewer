from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class QuestionResponseDTO(BaseModel):
    question_id: UUID
    text: str
    interview_id: UUID
    question_order: int
    created_at: datetime

    class Config:
        from_attributes = True


class GenerateQuestionDTO(BaseModel):
    interview_id: UUID
    topic: str
    previous_answers: list[str] = []
