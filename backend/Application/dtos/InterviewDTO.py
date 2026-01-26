from typing import Optional
from pydantic import BaseModel

from Domain.Enums import InterviewStatus


class CreateInterviewDTO(BaseModel):
    topic: str


class UpdateInterviewDTO(BaseModel):
    topic: Optional[str] = None
    status: Optional[InterviewStatus] = None