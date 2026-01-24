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
        pass
    
    async def get_by_id(self, answer_id: UUID) -> Optional[Answer]:
        pass
    
    async def get_by_interview_id(self, interview_id: UUID) -> List[Answer]:
        pass
    
    async def get_by_question_id(self, question_id: UUID) -> List[Answer]:
        pass
