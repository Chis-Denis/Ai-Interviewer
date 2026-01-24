from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from Domain.Entities import Question
from Application.RepositoryInterfaces import QuestionRepository
from Infrastructure.Db.models import QuestionModel
from Infrastructure.Db.mappers import (
    question_model_to_entity,
    question_entity_to_model,
)


class SqlQuestionRepository(QuestionRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, question: Question) -> Question:
        model = question_entity_to_model(question)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return question_model_to_entity(model)
    
    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        model = self.db.query(QuestionModel).filter(QuestionModel.question_id == str(question_id)).first()
        if not model:
            return None
        return question_model_to_entity(model)
    
    async def get_by_interview_id(self, interview_id: UUID) -> List[Question]:
        models = self.db.query(QuestionModel).filter(QuestionModel.interview_id == str(interview_id)).order_by(QuestionModel.question_order).all()
        return [question_model_to_entity(model) for model in models]
