from typing import Optional, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from Domain.Entities import Question
from Application.RepositoryInterfaces import QuestionRepository
from Infrastructure.Db.models import QuestionModel
from Infrastructure.Db.mappers import (
    question_model_to_entity,
    question_entity_to_model,
)


class SqlQuestionRepository(QuestionRepository):
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, question: Question) -> Question:
        try:
            model = question_entity_to_model(question)
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return question_model_to_entity(model)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
    
    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        try:
            result = await self.db.execute(
                select(QuestionModel).filter(QuestionModel.question_id == str(question_id))
            )
            model = result.scalar_one_or_none()
            if not model:
                return None
            return question_model_to_entity(model)
        except SQLAlchemyError:
            raise
    
    async def get_by_interview_id(self, interview_id: UUID) -> List[Question]:
        try:
            result = await self.db.execute(
                select(QuestionModel)
                .filter(QuestionModel.interview_id == str(interview_id))
                .order_by(QuestionModel.question_order)
            )
            models = result.scalars().all()
            return [question_model_to_entity(model) for model in models]
        except SQLAlchemyError:
            raise
