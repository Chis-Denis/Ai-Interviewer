from uuid import UUID

from Domain.Entities import InterviewSummary
from Domain.Enums import InterviewStatus

from Application.RepositoryInterfaces import (
    InterviewRepository,
    AnswerRepository,
    InterviewSummaryRepository,
    QuestionRepository,
)
from Application.Services.LLMOrchestrator import LLMOrchestrator
from Application.Services.llm_data import QuestionData, AnswerData
from Application.DTOs import LlmSummaryResponseDTO
from Application.Exceptions import InterviewNotFoundException, NoAnswersFoundException, SummaryNotFoundException, ValidationException
from Application.Analysis.AnswerEvaluator import AnswerEvaluator
from Application.Analysis.scoring import ScoringCalculator


class GenerateSummaryUseCase:
    
    def __init__(
        self,
        interview_repository: InterviewRepository,
        answer_repository: AnswerRepository,
        summary_repository: InterviewSummaryRepository,
        question_repository: QuestionRepository,
        llm_orchestrator: LLMOrchestrator,
    ):
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.summary_repository = summary_repository
        self.question_repository = question_repository
        self.llm_orchestrator = llm_orchestrator
    
    async def execute(self, interview_id: UUID) -> InterviewSummary:
        interview = await self.interview_repository.get_by_id(interview_id)
        if not interview:
            raise InterviewNotFoundException(interview_id)
        
        answers = await self.answer_repository.get_by_interview_id(interview_id)
        if not answers:
            raise NoAnswersFoundException(interview_id)
        
        questions = await self.question_repository.get_by_interview_id(interview_id)
        
        question_data_list = [
            QuestionData(text=question.text, question_order=question.question_order, question_id=question.question_id)
            for question in questions
        ]
        
        answer_data_list = [
            AnswerData(text=answer.text, question_id=answer.question_id)
            for answer in answers
        ]
        
        llm_summary_dict = await self.llm_orchestrator.generate_summary(
            interview_topic=interview.topic,
            answers=answer_data_list,
            questions=question_data_list,
        )
        
        try:
            llm_summary = LlmSummaryResponseDTO(**llm_summary_dict)
        except ValidationException:
            raise
        except Exception as e:
            raise ValidationException(f"Failed to validate LLM summary response: {str(e)}") from e
        
        evaluation_result = AnswerEvaluator.evaluate_all_answers(answer_data_list)
        scoring_result = ScoringCalculator.calculate_all_scores(answer_data_list)
        
        summary = InterviewSummary(
            interview_id=interview_id,
            themes=llm_summary.themes,
            key_points=llm_summary.key_points,
            sentiment_score=llm_summary.sentiment_score,
            sentiment_label=llm_summary.sentiment_label.value,
            confidence_score=evaluation_result['confidence_score'],
            clarity_score=evaluation_result['clarity_score'],
            strengths=llm_summary.strengths,
            weaknesses=llm_summary.weaknesses,
            consistency_score=scoring_result['consistency_score'],
            missing_information=llm_summary.missing_information,
            overall_usefulness=scoring_result['overall_usefulness'],
            full_summary_text=llm_summary.full_summary_text,
        )
        
        existing_summary = await self.summary_repository.get_by_interview_id(interview_id)
        if existing_summary:
            summary.summary_id = existing_summary.summary_id
            updated_summary = await self.summary_repository.update(summary)
            if not updated_summary:
                raise SummaryNotFoundException(interview_id)
        else:
            updated_summary = await self.summary_repository.create(summary)
        
        if interview.status != InterviewStatus.COMPLETED:
            interview.complete()
            await self.interview_repository.update(interview)
        
        return updated_summary
