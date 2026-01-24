from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime


class QuestionResponseDTO(BaseModel):
    question_id: UUID
    text: str
    interview_id: UUID
    question_order: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.astimezone().strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True


class GenerateQuestionDTO(BaseModel):
    interview_id: UUID
    topic: str
    previous_answers: list[str] = []
