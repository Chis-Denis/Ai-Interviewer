from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from Domain.Entities import InterviewSummary


class InterviewSummaryRepository(ABC):
    
    @abstractmethod
    async def create(self, summary: InterviewSummary) -> InterviewSummary:
        pass
    
    @abstractmethod
    async def get_by_interview_id(self, interview_id: UUID) -> Optional[InterviewSummary]:
        pass
    
    @abstractmethod
    async def update(self, summary: InterviewSummary) -> Optional[InterviewSummary]:
        pass
