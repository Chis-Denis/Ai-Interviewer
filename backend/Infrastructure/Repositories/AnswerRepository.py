from typing import Optional, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from Domain.Entities import Answer
from Application.RepositoryInterfaces import AnswerRepository
from Infrastructure.Db.models import AnswerModel
from Infrastructure.Db.mappers import (
    answer_model_to_entity,
    answer_entity_to_model,
)


class SqlAnswerRepository(AnswerRepository):
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, answer: Answer) -> Answer:
        try:
            model = answer_entity_to_model(answer)
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return answer_model_to_entity(model)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise
    
    async def get_by_id(self, answer_id: UUID) -> Optional[Answer]:
        try:
            result = await self.db.execute(
                select(AnswerModel).filter(AnswerModel.answer_id == str(answer_id))
            )
            model = result.scalar_one_or_none()
            if not model:
                return None
            return answer_model_to_entity(model)
        except SQLAlchemyError as e:
            raise
    
    async def get_by_interview_id(self, interview_id: UUID) -> List[Answer]:
        try:
            result = await self.db.execute(
                select(AnswerModel)
                .filter(AnswerModel.interview_id == str(interview_id))
                .order_by(AnswerModel.created_at)
            )
            models = result.scalars().all()
            return [answer_model_to_entity(model) for model in models]
        except SQLAlchemyError as e:
            raise
    
    async def get_by_question_id(self, question_id: UUID) -> List[Answer]:
        try:
            result = await self.db.execute(
                select(AnswerModel)
                .filter(AnswerModel.question_id == str(question_id))
                .order_by(AnswerModel.created_at)
            )
            models = result.scalars().all()
            return [answer_model_to_entity(model) for model in models]
        except SQLAlchemyError as e:
            raise
