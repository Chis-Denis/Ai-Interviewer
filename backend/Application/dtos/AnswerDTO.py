from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreateAnswerDTO(BaseModel):
    text: str
    question_id: UUID
    interview_id: UUID


class AnswerResponseDTO(BaseModel):
    answer_id: UUID
    text: str
    question_id: UUID
    interview_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
