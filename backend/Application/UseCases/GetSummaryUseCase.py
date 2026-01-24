from uuid import UUID
from Domain.Entities import InterviewSummary
from Application.RepositoryInterfaces import InterviewSummaryRepository
from Application.Exceptions import SummaryNotFoundException


class GetSummaryUseCase:
    
    def __init__(self, summary_repository: InterviewSummaryRepository):
        self.summary_repository = summary_repository
    
    async def execute(self, interview_id: UUID) -> InterviewSummary:
        summary = await self.summary_repository.get_by_interview_id(interview_id)
        if not summary:
            raise SummaryNotFoundException(str(interview_id))
        return summary
