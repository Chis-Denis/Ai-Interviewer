from uuid import UUID

from domain.entities import InterviewSummary
from application.repository_interfaces import InterviewSummaryRepository
from application.exceptions import SummaryNotFoundException
from application.use_cases.base_use_case import BaseUseCase


class GetSummaryUseCase(BaseUseCase[InterviewSummary, InterviewSummaryRepository]):
    
    async def execute(self, interview_id: UUID) -> InterviewSummary:
        summary = await self.repository.get_by_interview_id(interview_id)
        if not summary:
            raise SummaryNotFoundException(interview_id)
        return summary
