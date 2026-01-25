from uuid import UUID

from Domain.Entities import InterviewSummary

from Application.RepositoryInterfaces import (
    InterviewRepository,
    AnswerRepository,
    InterviewSummaryRepository,
    QuestionRepository,
)
from Application.Service import LlmService
from Application.Exceptions import InterviewNotFoundException, NoAnswersFoundException, SummaryNotFoundException


class GenerateSummaryUseCase:
    
    def __init__(
        self,
        interview_repository: InterviewRepository,
        answer_repository: AnswerRepository,
        summary_repository: InterviewSummaryRepository,
        question_repository: QuestionRepository,
        llm_service: LlmService,
    ):
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.summary_repository = summary_repository
        self.question_repository = question_repository
        self.llm_service = llm_service
    
    async def execute(self, interview_id: UUID) -> InterviewSummary:
        interview = await self.interview_repository.get_by_id(interview_id)
        if not interview:
            raise InterviewNotFoundException(interview_id)
        
        answers = await self.answer_repository.get_by_interview_id(interview_id)
        if not answers:
            raise NoAnswersFoundException(interview_id)
        
        questions = await self.question_repository.get_by_interview_id(interview_id)
        
        summary_data = await self.llm_service.generate_summary(
            interview_topic=interview.topic,
            answers=answers,
            questions=questions,
        )
        
        summary = InterviewSummary(
            interview_id=interview_id,
            themes=summary_data["themes"],
            key_points=summary_data["key_points"],
            sentiment_score=summary_data["sentiment_score"],
            sentiment_label=summary_data["sentiment_label"],
            full_summary_text=summary_data["full_summary_text"],
        )
        
        existing_summary = await self.summary_repository.get_by_interview_id(interview_id)
        if existing_summary:
            summary.summary_id = existing_summary.summary_id
            updated_summary = await self.summary_repository.update(summary)
            if not updated_summary:
                raise SummaryNotFoundException(interview_id)
            return updated_summary
        
        return await self.summary_repository.create(summary)
