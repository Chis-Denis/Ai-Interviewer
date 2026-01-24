from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from Domain.Entities import InterviewSummary
from Application.RepositoryInterfaces import InterviewSummaryRepository
from Application.Exceptions import SummaryNotFoundException
from Infrastructure.Db.models import InterviewSummaryModel
from Infrastructure.Db.mappers import (
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
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise
    
    async def get_by_interview_id(self, interview_id: UUID) -> Optional[InterviewSummary]:
        try:
            result = await self.db.execute(
                select(InterviewSummaryModel).filter(InterviewSummaryModel.interview_id == str(interview_id))
            )
            model = result.scalar_one_or_none()
            if not model:
                return None
            return interview_summary_model_to_entity(model)
        except SQLAlchemyError as e:
            raise
    
    async def update(self, summary: InterviewSummary) -> InterviewSummary:
        try:
            result = await self.db.execute(
                select(InterviewSummaryModel).filter(InterviewSummaryModel.summary_id == str(summary.summary_id))
            )
            model = result.scalar_one_or_none()
            if not model:
                raise SummaryNotFoundException(summary.interview_id)
            model.themes = summary.themes
            model.key_points = summary.key_points
            model.sentiment_score = summary.sentiment_score
            model.sentiment_label = summary.sentiment_label
            model.full_summary_text = summary.full_summary_text
            await self.db.commit()
            await self.db.refresh(model)
            return interview_summary_model_to_entity(model)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise
