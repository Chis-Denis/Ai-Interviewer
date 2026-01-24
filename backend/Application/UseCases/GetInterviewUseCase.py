from typing import List
from uuid import UUID
from Domain.Entities import Interview
from Application.RepositoryInterfaces import InterviewRepository
from Application.Exceptions import InterviewNotFoundException


class GetInterviewUseCase:
    
    def __init__(self, interview_repository: InterviewRepository):
        self.interview_repository = interview_repository
    
    async def execute(self, interview_id: UUID) -> Interview:
        interview = await self.interview_repository.get_by_id(interview_id)
        if not interview:
            raise InterviewNotFoundException(str(interview_id))
        return interview
    
    async def execute_all(self) -> List[Interview]:
        return await self.interview_repository.get_all()