from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from Domain.Entities import Question


class QuestionRepository(ABC):
    
    @abstractmethod
    async def create(self, question: Question) -> Question:
        pass
    
    @abstractmethod
    async def get_by_id(self, question_id: UUID) -> Optional[Question]:
        pass
    
    @abstractmethod
    async def get_by_interview_id(self, interview_id: UUID) -> List[Question]:
        pass