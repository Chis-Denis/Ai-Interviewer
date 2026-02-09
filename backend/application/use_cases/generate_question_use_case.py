from domain.entities import Question
from domain.enums import InterviewStatus

from application.repository_interfaces import QuestionRepository, InterviewRepository, AnswerRepository
from application.services.llm_orchestrator import LLMOrchestrator
from application.services.llm_data import QuestionData, AnswerData
from application.dtos import GenerateQuestionDTO
from application.exceptions import (
    InterviewNotFoundException,
    InterviewAlreadyCompletedException,
    MaxQuestionsReachedException,
)


class GenerateQuestionUseCase:
    
    def __init__(
        self,
        question_repository: QuestionRepository,
        interview_repository: InterviewRepository,
        answer_repository: AnswerRepository,
        llm_orchestrator: LLMOrchestrator,
        max_questions_per_interview: int,
    ):
        self.question_repository = question_repository
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.llm_orchestrator = llm_orchestrator
        self.max_questions_per_interview = max_questions_per_interview
    
    async def execute(self, dto: GenerateQuestionDTO) -> Question:
        interview = await self.interview_repository.get_by_id(dto.interview_id)
        if not interview:
            raise InterviewNotFoundException(dto.interview_id)
        
        if interview.status == InterviewStatus.COMPLETED:
            raise InterviewAlreadyCompletedException(dto.interview_id)
        
        existing_questions = await self.question_repository.get_by_interview_id(dto.interview_id)
        
        if len(existing_questions) >= self.max_questions_per_interview:
            raise MaxQuestionsReachedException(dto.interview_id, self.max_questions_per_interview)
        
        if interview.status == InterviewStatus.NOT_STARTED:
            interview.start()
            await self.interview_repository.update(interview)
        
        next_order = len(existing_questions) + 1
        
        previous_answers = await self.answer_repository.get_by_interview_id(dto.interview_id)
        
        question_data_list = [
            QuestionData(text=question.text, question_order=question.question_order, question_id=question.question_id)
            for question in existing_questions
        ] if existing_questions else None
        
        answer_data_list = [
            AnswerData(text=answer.text, question_id=answer.question_id)
            for answer in previous_answers
        ] if previous_answers else None
        
        question_text = await self.llm_orchestrator.generate_question(
            topic=interview.topic,
            existing_questions=question_data_list,
            previous_answers=answer_data_list,
        )
        
        question = Question(
            text=question_text,
            interview_id=dto.interview_id,
            question_order=next_order,
        )
        
        return await self.question_repository.create(question)
