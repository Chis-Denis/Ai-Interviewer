from Domain.Entities import Question
from Domain.Enums import InterviewStatus

from Application.RepositoryInterfaces import QuestionRepository, InterviewRepository
from Application.dtos import GenerateQuestionDTO
from Application.Exceptions import (
    InterviewNotFoundException,
    InterviewAlreadyCompletedException,
    MaxQuestionsReachedException,
    InterviewNotInProgressException,
)
from Core.config import settings


class GenerateQuestionUseCase:
    
    def __init__(
        self,
        question_repository: QuestionRepository,
        interview_repository: InterviewRepository,
    ):
        self.question_repository = question_repository
        self.interview_repository = interview_repository
    
    async def execute(self, dto: GenerateQuestionDTO) -> Question:
        interview = await self.interview_repository.get_by_id(dto.interview_id)
        if not interview:
            raise InterviewNotFoundException(dto.interview_id)
        
        # Business rule: Interview must not be completed
        if interview.status == InterviewStatus.COMPLETED:
            raise InterviewAlreadyCompletedException(dto.interview_id)
        
        # Business rule: Interview must not be cancelled
        if interview.status == InterviewStatus.CANCELLED:
            raise InterviewNotInProgressException(
                dto.interview_id,
                interview.status.value
            )
        
        existing_questions = await self.question_repository.get_by_interview_id(dto.interview_id)
        
        # Business rule: Check max questions reached
        max_questions = settings.MAX_QUESTIONS_PER_INTERVIEW
        if len(existing_questions) >= max_questions:
            raise MaxQuestionsReachedException(dto.interview_id, max_questions)
        
        next_order = len(existing_questions) + 1
        
        question_text = f"Tell me about {dto.topic}"
        if existing_questions:
            question_text = f"Based on your previous answers, can you elaborate more on {dto.topic}?"
        
        question = Question(
            text=question_text,
            interview_id=dto.interview_id,
            question_order=next_order,
        )
        
        return await self.question_repository.create(question)
