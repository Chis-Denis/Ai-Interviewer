from uuid import UUID
from Application.RepositoryInterfaces import InterviewRepository


class DeleteInterviewUseCase:
    
    def __init__(self, interview_repository: InterviewRepository):
        self.interview_repository = interview_repository
    
    async def execute(self, interview_id: UUID) -> bool:
        return await self.interview_repository.delete(interview_id)
