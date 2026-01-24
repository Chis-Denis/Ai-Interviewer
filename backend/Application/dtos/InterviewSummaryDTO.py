from pydantic import BaseModel
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

    class Config:
        from_attributes = True
