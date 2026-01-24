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
        pass
    
    async def get_by_interview_id(self, interview_id: UUID) -> Optional[InterviewSummary]:
        pass
    
    async def update(self, summary: InterviewSummary) -> InterviewSummary:
        pass
