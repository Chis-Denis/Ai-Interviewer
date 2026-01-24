from pydantic import BaseModel, field_serializer, field_validator
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
    
    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Topic is required and cannot be empty")
        if len(v.strip()) < 3:
            raise ValueError("Topic must be at least 3 characters long")
        if len(v) > 200:
            raise ValueError("Topic must be at most 200 characters long")
        return v.strip()
    
    @field_validator('previous_answers')
    @classmethod
    def validate_previous_answers(cls, v: list[str]) -> list[str]:
        if not isinstance(v, list):
            raise ValueError("Previous answers must be a list")
        for answer in v:
            if not isinstance(answer, str):
                raise ValueError("All previous answers must be strings")
            if len(answer) > 5000:
                raise ValueError("Each answer must be at most 5000 characters long")
        return v