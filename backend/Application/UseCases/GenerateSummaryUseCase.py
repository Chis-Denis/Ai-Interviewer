from uuid import UUID

from Domain.Entities import InterviewSummary

from Application.RepositoryInterfaces import (
    InterviewRepository,
    AnswerRepository,
    InterviewSummaryRepository,
    QuestionRepository,
)
from Application.Service import LlmService
from Application.Service.llm_data import QuestionData, AnswerData
from Application.dtos import SummaryResponseDTO
from Application.Exceptions import InterviewNotFoundException, NoAnswersFoundException, SummaryNotFoundException, ValidationException


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
        
        question_data_list = [
            QuestionData(text=q.text, question_order=q.question_order, question_id=q.question_id)
            for q in questions
        ]
        
        answer_data_list = [
            AnswerData(text=a.text, question_id=a.question_id)
            for a in answers
        ]
        
        summary_data_dict = await self.llm_service.generate_summary(
            interview_topic=interview.topic,
            answers=answer_data_list,
            questions=question_data_list,
        )
        
        try:
            summary_response = SummaryResponseDTO(**summary_data_dict)
        except ValidationException:
            raise
        except Exception as e:
            raise ValidationException(f"Failed to validate summary response: {str(e)}")
        
        summary = InterviewSummary(
            interview_id=interview_id,
            themes=summary_response.themes,
            key_points=summary_response.key_points,
            sentiment_score=summary_response.sentiment_score,
            sentiment_label=summary_response.sentiment_label.value,
            full_summary_text=summary_response.full_summary_text,
        )
        
        existing_summary = await self.summary_repository.get_by_interview_id(interview_id)
        if existing_summary:
            summary.summary_id = existing_summary.summary_id
            updated_summary = await self.summary_repository.update(summary)
            if not updated_summary:
                raise SummaryNotFoundException(interview_id)
            return updated_summary
        
        return await self.summary_repository.create(summary)
