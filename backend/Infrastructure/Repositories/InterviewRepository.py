from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from Domain.Entities import Interview
from Application.RepositoryInterfaces import InterviewRepository
from Infrastructure.Db.models import InterviewModel
from Infrastructure.Db.mappers import (
    interview_model_to_entity,
    interview_entity_to_model,
)


class SqlInterviewRepository(InterviewRepository):
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, interview: Interview) -> Interview:
        pass
    
    async def get_by_id(self, interview_id: UUID) -> Optional[Interview]:
        pass
    
    async def update(self, interview: Interview) -> Interview:
        pass
    
    async def delete(self, interview_id: UUID) -> bool:
        pass
    
    async def get_all(self) -> List[Interview]:
        pass
