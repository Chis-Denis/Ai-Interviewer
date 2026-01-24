from Domain.Entities import Interview
from Application.RepositoryInterfaces import InterviewRepository
from Application.dtos import CreateInterviewDTO


class CreateInterviewUseCase:
    
    def __init__(self, interview_repository: InterviewRepository):
        self.interview_repository = interview_repository
    
    async def execute(self, dto: CreateInterviewDTO) -> Interview:
        pass
