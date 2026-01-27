from domain.entities import Interview

from application.repository_interfaces import InterviewRepository
from application.dtos import CreateInterviewDTO


class CreateInterviewUseCase:
    
    def __init__(self, interview_repository: InterviewRepository):
        self.interview_repository = interview_repository
    
    async def execute(self, dto: CreateInterviewDTO) -> Interview:
        interview = Interview(topic=dto.topic)
        return await self.interview_repository.create(interview)
