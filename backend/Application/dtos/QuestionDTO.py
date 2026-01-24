from datetime import datetime, timezone
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator

from Presentation.Validations.validators import validate_string_length, validate_uuid


class QuestionResponseDTO(BaseModel):
    question_id: UUID
    text: str
    interview_id: UUID
    question_order: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        local_time = value.astimezone()
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True


class GenerateQuestionDTO(BaseModel):
    interview_id: UUID
    topic: str
    previous_answers: List[str] = []
    
    @field_validator('interview_id')
    @classmethod
    def validate_interview_id(cls, v) -> UUID:
        return validate_uuid(v)
    
    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v: str) -> str:
        return validate_string_length(v, min_length=3, max_length=200)
    
    @field_validator('previous_answers')
    @classmethod
    def validate_previous_answers(cls, v: List[str]) -> List[str]:
        if not isinstance(v, list):
            raise ValueError("Previous answers must be a list")
        for answer in v:
            if not isinstance(answer, str):
                raise ValueError("All previous answers must be strings")
            validate_string_length(answer, min_length=0, max_length=5000)
        return v