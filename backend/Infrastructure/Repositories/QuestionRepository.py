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
        pass
    
    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        pass
    
    async def get_by_interview_id(self, interview_id: UUID) -> List[Question]:
        pass
    
    async def update(self, question: Question) -> Question:
        pass
