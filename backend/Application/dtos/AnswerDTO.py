from pydantic import BaseModel, field_serializer
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

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.astimezone().strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True
