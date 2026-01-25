from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4


class InterviewSummary:
    
    def __init__(
        self,
        interview_id: UUID,
        themes: List[str],
        key_points: List[str],
        summary_id: Optional[UUID] = None,
        sentiment_score: Optional[float] = None,
        sentiment_label: Optional[str] = None,
        confidence_score: Optional[float] = None,
        clarity_score: Optional[float] = None,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        consistency_score: Optional[float] = None,
        missing_information: Optional[List[str]] = None,
        overall_usefulness: Optional[float] = None,
        full_summary_text: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.summary_id = summary_id or uuid4()
        self.interview_id = interview_id
        self.themes = themes or []
        self.key_points = key_points or []
        self.sentiment_score = sentiment_score
        self.sentiment_label = sentiment_label
        self.confidence_score = confidence_score
        self.clarity_score = clarity_score
        self.strengths = strengths or []
        self.weaknesses = weaknesses or []
        self.consistency_score = consistency_score
        self.missing_information = missing_information or []
        self.overall_usefulness = overall_usefulness
        self.full_summary_text = full_summary_text
        self.created_at = created_at or datetime.now(timezone.utc)
    
    def __repr__(self) -> str:
        return f"<InterviewSummary(id={self.summary_id}, interview_id={self.interview_id}, themes={len(self.themes)})>"
