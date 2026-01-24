from Domain.Entities import InterviewSummary
from Application.RepositoryInterfaces import (
    InterviewRepository,
    AnswerRepository,
    InterviewSummaryRepository,
)
from uuid import UUID
from Application.Exceptions import InterviewNotFoundException, NoAnswersFoundException


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
        interview = await self.interview_repository.get_by_id(interview_id)
        if not interview:
            raise InterviewNotFoundException(str(interview_id))
        
        answers = await self.answer_repository.get_by_interview_id(interview_id)
        if not answers:
            raise NoAnswersFoundException(str(interview_id))
        
        answer_texts = [answer.text for answer in answers]
        combined_text = " ".join(answer_texts)
        
        themes = [f"Theme {i+1}" for i in range(min(3, len(answers)))]
        key_points = [f"Key point from answer {i+1}" for i in range(min(5, len(answers)))]
        
        summary = InterviewSummary(
            interview_id=interview_id,
            themes=themes,
            key_points=key_points,
            sentiment_score=0.5,
            sentiment_label="neutral",
            full_summary_text=f"Summary of interview about {interview.topic}. Total answers: {len(answers)}",
        )
        
        existing_summary = await self.summary_repository.get_by_interview_id(interview_id)
        if existing_summary:
            summary.summary_id = existing_summary.summary_id
            return await self.summary_repository.update(summary)
        
        return await self.summary_repository.create(summary)
