from Domain.Entities import Question
from Domain.Enums import InterviewStatus

from Application.RepositoryInterfaces import QuestionRepository, InterviewRepository, AnswerRepository
from Application.Service import LlmService
from Application.Service.llm_data import QuestionData, AnswerData
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
        max_questions_per_interview: int,
    ):
        self.question_repository = question_repository
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.llm_service = llm_service
        self.max_questions_per_interview = max_questions_per_interview
    
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
        
        if len(existing_questions) >= self.max_questions_per_interview:
            raise MaxQuestionsReachedException(dto.interview_id, self.max_questions_per_interview)
        
        if interview.status == InterviewStatus.NOT_STARTED:
            interview.start()
            await self.interview_repository.update(interview)
        
        next_order = len(existing_questions) + 1
        
        previous_answers = await self.answer_repository.get_by_interview_id(dto.interview_id)
        
        question_data_list = [
            QuestionData(text=q.text, question_order=q.question_order, question_id=q.question_id)
            for q in existing_questions
        ] if existing_questions else None
        
        answer_data_list = [
            AnswerData(text=a.text, question_id=a.question_id)
            for a in previous_answers
        ] if previous_answers else None
        
        question_text = await self.llm_service.generate_question(
            topic=interview.topic,
            interview_id=dto.interview_id,
            existing_questions=question_data_list,
            previous_answers=answer_data_list,
        )
        
        question = Question(
            text=question_text,
            interview_id=dto.interview_id,
            question_order=next_order,
        )
        
        return await self.question_repository.create(question)
