from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator

from Presentation.Validations.validators import validate_string_length, validate_uuid


class CreateAnswerDTO(BaseModel):
    text: str
    question_id: UUID
    interview_id: UUID
    
    @field_validator('question_id', 'interview_id')
    @classmethod
    def validate_uuids(cls, v) -> UUID:
        return validate_uuid(v)
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        return validate_string_length(v, min_length=10, max_length=10000)


class AnswerResponseDTO(BaseModel):
    answer_id: UUID
    text: str
    question_id: UUID
    interview_id: UUID
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        local_time = value.astimezone()
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True
