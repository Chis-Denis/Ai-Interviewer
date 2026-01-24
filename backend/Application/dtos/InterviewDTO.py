from pydantic import BaseModel, field_serializer, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime, timezone
from Domain.Enums import InterviewStatus


class CreateInterviewDTO(BaseModel):
    topic: str
    
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
        if not v.strip():
            raise ValueError("Topic cannot be empty")
        if len(v.strip()) < 3:
            raise ValueError("Topic must be at least 3 characters long")
        if len(v) > 200:
            raise ValueError("Topic must be at most 200 characters long")
        return v.strip()