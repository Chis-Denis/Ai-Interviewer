from pydantic import BaseModel, field_serializer
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class InterviewSummaryResponseDTO(BaseModel):
    summary_id: UUID
    interview_id: UUID
    themes: List[str]
    key_points: List[str]
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    full_summary_text: Optional[str] = None
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.astimezone().strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True
