from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from domain.entities import InterviewSummary
from application.repository_interfaces import InterviewSummaryRepository
from infrastructure.database.models import InterviewSummaryModel
from infrastructure.database.mappers import (
    interview_summary_model_to_entity,
    interview_summary_entity_to_model,
)


class SqlInterviewSummaryRepository(InterviewSummaryRepository):
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, summary: InterviewSummary) -> InterviewSummary:
        try:
            model = interview_summary_entity_to_model(summary)
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return interview_summary_model_to_entity(model)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
    
    async def get_by_interview_id(self, interview_id: UUID) -> Optional[InterviewSummary]:
        result = await self.db.execute(
            select(InterviewSummaryModel).filter(InterviewSummaryModel.interview_id == str(interview_id))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return interview_summary_model_to_entity(model)

