from typing import Optional, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from domain.entities import Interview
from application.repository_interfaces import InterviewRepository
from infrastructure.database.models import InterviewModel
from infrastructure.database.mappers import (
    interview_model_to_entity,
    interview_entity_to_model,
)


class SqlInterviewRepository(InterviewRepository):
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, interview: Interview) -> Interview:
        try:
            model = interview_entity_to_model(interview)
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return interview_model_to_entity(model)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
    
    async def get_by_id(self, interview_id: UUID) -> Optional[Interview]:
        result = await self.db.execute(
            select(InterviewModel).filter(InterviewModel.interview_id == str(interview_id))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return interview_model_to_entity(model)
    
    async def update(self, interview: Interview) -> Optional[Interview]:
        try:
            result = await self.db.execute(
                select(InterviewModel).filter(InterviewModel.interview_id == str(interview.interview_id))
            )
            model = result.scalar_one_or_none()
            if not model:
                return None
            model.topic = interview.topic
            model.status = interview.status.value
            model.updated_at = interview.updated_at
            model.completed_at = interview.completed_at
            await self.db.commit()
            await self.db.refresh(model)
            return interview_model_to_entity(model)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
    
    async def delete(self, interview_id: UUID) -> bool:
        try:
            result = await self.db.execute(
                delete(InterviewModel).filter(InterviewModel.interview_id == str(interview_id))
            )
            await self.db.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.db.rollback()
            raise
    
    async def get_all(self) -> List[Interview]:
        result = await self.db.execute(select(InterviewModel))
        models = result.scalars().all()
        return [interview_model_to_entity(model) for model in models]
