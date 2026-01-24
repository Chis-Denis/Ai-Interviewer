from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from Domain.Entities import Answer
from Application.RepositoryInterfaces import AnswerRepository
from Infrastructure.Db.models import AnswerModel
from Infrastructure.Db.mappers import (
    answer_model_to_entity,
    answer_entity_to_model,
)


class SqlAnswerRepository(AnswerRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, answer: Answer) -> Answer:
        model = answer_entity_to_model(answer)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return answer_model_to_entity(model)
    
    async def get_by_id(self, answer_id: UUID) -> Optional[Answer]:
        model = self.db.query(AnswerModel).filter(AnswerModel.answer_id == str(answer_id)).first()
        if not model:
            return None
        return answer_model_to_entity(model)
    
    async def get_by_interview_id(self, interview_id: UUID) -> List[Answer]:
        models = self.db.query(AnswerModel).filter(AnswerModel.interview_id == str(interview_id)).order_by(AnswerModel.created_at).all()
        return [answer_model_to_entity(model) for model in models]
    
    async def get_by_question_id(self, question_id: UUID) -> List[Answer]:
        models = self.db.query(AnswerModel).filter(AnswerModel.question_id == str(question_id)).order_by(AnswerModel.created_at).all()
        return [answer_model_to_entity(model) for model in models]
