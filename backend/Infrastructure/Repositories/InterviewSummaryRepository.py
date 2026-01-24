from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from Domain.Entities import InterviewSummary
from Application.RepositoryInterfaces import InterviewSummaryRepository
from Infrastructure.Db.models import InterviewSummaryModel
from Infrastructure.Db.mappers import (
    interview_summary_model_to_entity,
    interview_summary_entity_to_model,
)


class SqlInterviewSummaryRepository(InterviewSummaryRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, summary: InterviewSummary) -> InterviewSummary:
        model = interview_summary_entity_to_model(summary)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return interview_summary_model_to_entity(model)
    
    async def get_by_interview_id(self, interview_id: UUID) -> Optional[InterviewSummary]:
        model = self.db.query(InterviewSummaryModel).filter(InterviewSummaryModel.interview_id == str(interview_id)).first()
        if not model:
            return None
        return interview_summary_model_to_entity(model)
    
    async def update(self, summary: InterviewSummary) -> InterviewSummary:
        model = self.db.query(InterviewSummaryModel).filter(InterviewSummaryModel.summary_id == str(summary.summary_id)).first()
        if not model:
            raise ValueError("Interview summary not found")
        model.themes = summary.themes
        model.key_points = summary.key_points
        model.sentiment_score = summary.sentiment_score
        model.sentiment_label = summary.sentiment_label
        model.full_summary_text = summary.full_summary_text
        self.db.commit()
        self.db.refresh(model)
        return interview_summary_model_to_entity(model)
