from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_serializer, field_validator

from Domain.Enums import InterviewStatus
from Presentation.Validations.validators import validate_string_length


class CreateInterviewDTO(BaseModel):
    topic: str
    
    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v: str) -> str:
        return validate_string_length(v, min_length=3, max_length=200)


class InterviewResponseDTO(BaseModel):
    interview_id: UUID
    topic: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    @field_serializer('created_at', 'updated_at', 'completed_at')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        local_time = value.astimezone()
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True


class UpdateInterviewDTO(BaseModel):
    topic: Optional[str] = None
    status: Optional[InterviewStatus] = None
    
    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_string_length(v, min_length=3, max_length=200)