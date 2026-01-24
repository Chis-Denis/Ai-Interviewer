from Domain.Entities import InterviewSummary
from Application.RepositoryInterfaces import (
    InterviewRepository,
    AnswerRepository,
    InterviewSummaryRepository,
)
from uuid import UUID


class GenerateSummaryUseCase:
    
    def __init__(
        self,
        interview_repository: InterviewRepository,
        answer_repository: AnswerRepository,
        summary_repository: InterviewSummaryRepository,
    ):
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.summary_repository = summary_repository
    
    async def execute(self, interview_id: UUID) -> InterviewSummary:
        pass
