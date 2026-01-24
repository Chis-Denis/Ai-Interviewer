from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
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

    class Config:
        from_attributes = True


class UpdateInterviewDTO(BaseModel):
    topic: Optional[str] = None
    status: Optional[InterviewStatus] = None
