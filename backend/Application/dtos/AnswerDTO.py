from pydantic import BaseModel, field_serializer, field_validator
from uuid import UUID
from datetime import datetime


class CreateAnswerDTO(BaseModel):
    text: str
    question_id: UUID
    interview_id: UUID
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Answer text is required and cannot be empty")
        if len(v.strip()) < 10:
            raise ValueError("Answer text must be at least 10 characters long")
        if len(v) > 10000:
            raise ValueError("Answer text must be at most 10000 characters long")
        return v.strip()


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
