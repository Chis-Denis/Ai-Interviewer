from Domain.Entities import Question
from Domain.Enums import InterviewStatus

from Application.RepositoryInterfaces import QuestionRepository, InterviewRepository, AnswerRepository
from Application.Service import LlmService
from Application.dtos import GenerateQuestionDTO
from Application.Exceptions import (
    InterviewNotFoundException,
    InterviewAlreadyCompletedException,
    MaxQuestionsReachedException,
    InterviewNotInProgressException,
)


class GenerateQuestionUseCase:
    
    def __init__(
        self,
        question_repository: QuestionRepository,
        interview_repository: InterviewRepository,
        answer_repository: AnswerRepository,
        llm_service: LlmService,
        settings: "Settings",
    ):
        self.question_repository = question_repository
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.llm_service = llm_service
        self.settings = settings
    
    async def execute(self, dto: GenerateQuestionDTO) -> Question:
        interview = await self.interview_repository.get_by_id(dto.interview_id)
        if not interview:
            raise InterviewNotFoundException(dto.interview_id)
        
        if interview.status == InterviewStatus.COMPLETED:
            raise InterviewAlreadyCompletedException(dto.interview_id)
        
        if interview.status == InterviewStatus.CANCELLED:
            raise InterviewNotInProgressException(
                dto.interview_id,
                interview.status.value
            )
        
        existing_questions = await self.question_repository.get_by_interview_id(dto.interview_id)
        
        max_questions = self.settings.MAX_QUESTIONS_PER_INTERVIEW
        if len(existing_questions) >= max_questions:
            raise MaxQuestionsReachedException(dto.interview_id, max_questions)
        
        next_order = len(existing_questions) + 1
        
        previous_answers = await self.answer_repository.get_by_interview_id(dto.interview_id)
        
        question_text = await self.llm_service.generate_question(
            topic=interview.topic,
            interview_id=dto.interview_id,
            existing_questions=existing_questions if existing_questions else None,
            previous_answers=previous_answers if previous_answers else None,
        )
        
        question = Question(
            text=question_text,
            interview_id=dto.interview_id,
            question_order=next_order,
        )
        
        return await self.question_repository.create(question)
