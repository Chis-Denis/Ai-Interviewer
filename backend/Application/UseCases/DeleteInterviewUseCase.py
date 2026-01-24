from uuid import UUID

from Application.RepositoryInterfaces import InterviewRepository
from Application.Exceptions import InterviewNotFoundException


class DeleteInterviewUseCase:
    
    def __init__(self, interview_repository: InterviewRepository):
        self.interview_repository = interview_repository
    
    async def execute(self, interview_id: UUID) -> None:
        deleted = await self.interview_repository.delete(interview_id)
        if not deleted:
            raise InterviewNotFoundException(interview_id)
