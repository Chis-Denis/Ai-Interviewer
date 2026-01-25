from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_serializer

from Domain.Enums import InterviewStatus


class CreateInterviewDTO(BaseModel):
    topic: str


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