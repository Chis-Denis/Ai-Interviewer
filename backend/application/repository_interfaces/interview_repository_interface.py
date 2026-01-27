from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from domain.entities import Interview


class InterviewRepository(ABC):
    
    @abstractmethod
    async def create(self, interview: Interview) -> Interview:
        pass
    
    @abstractmethod
    async def get_by_id(self, interview_id: UUID) -> Optional[Interview]:
        pass
    
    @abstractmethod
    async def update(self, interview: Interview) -> Optional[Interview]:
        pass
    
    @abstractmethod
    async def delete(self, interview_id: UUID) -> bool:
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Interview]:
        pass
