from typing import Optional, List
from uuid import UUID
from Domain.Entities import Interview
from Application.RepositoryInterfaces import InterviewRepository


class GetInterviewUseCase:
    
    def __init__(self, interview_repository: InterviewRepository):
        self.interview_repository = interview_repository
    
    async def execute(self, interview_id: UUID) -> Optional[Interview]:
        pass
    
    async def execute_all(self) -> List[Interview]:
        pass