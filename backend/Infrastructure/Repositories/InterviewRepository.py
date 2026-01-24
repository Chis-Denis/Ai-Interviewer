from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from Domain.Entities import Interview
from Application.RepositoryInterfaces import InterviewRepository
from Application.Exceptions import InterviewNotFoundException
from Infrastructure.Db.models import InterviewModel
from Infrastructure.Db.mappers import (
    interview_model_to_entity,
    interview_entity_to_model,
)


class SqlInterviewRepository(InterviewRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, interview: Interview) -> Interview:
        model = interview_entity_to_model(interview)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return interview_model_to_entity(model)
    
    async def get_by_id(self, interview_id: UUID) -> Optional[Interview]:
        model = self.db.query(InterviewModel).filter(InterviewModel.interview_id == str(interview_id)).first()
        if not model:
            return None
        return interview_model_to_entity(model)
    
    async def update(self, interview: Interview) -> Interview:
        model = self.db.query(InterviewModel).filter(InterviewModel.interview_id == str(interview.interview_id)).first()
        if not model:
            raise InterviewNotFoundException(interview.interview_id)
        model.topic = interview.topic
        model.status = interview.status.value
        model.updated_at = interview.updated_at
        model.completed_at = interview.completed_at
        self.db.commit()
        self.db.refresh(model)
        return interview_model_to_entity(model)
    
    async def delete(self, interview_id: UUID) -> bool:
        model = self.db.query(InterviewModel).filter(InterviewModel.interview_id == str(interview_id)).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
    
    async def get_all(self) -> List[Interview]:
        models = self.db.query(InterviewModel).all()
        return [interview_model_to_entity(model) for model in models]
