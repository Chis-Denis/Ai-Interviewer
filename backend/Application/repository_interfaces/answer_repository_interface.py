from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from domain.entities import Answer


class AnswerRepository(ABC):
    
    @abstractmethod
    async def create(self, answer: Answer) -> Answer:
        pass
    
    @abstractmethod
    async def get_by_id(self, answer_id: UUID) -> Optional[Answer]:
        pass
    
    @abstractmethod
    async def get_by_interview_id(self, interview_id: UUID) -> List[Answer]:
        pass
    
    @abstractmethod
    async def get_by_question_id(self, question_id: UUID) -> List[Answer]:
        pass
