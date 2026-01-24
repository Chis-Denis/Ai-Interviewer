from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_serializer


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
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        local_time = value.astimezone()
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True
