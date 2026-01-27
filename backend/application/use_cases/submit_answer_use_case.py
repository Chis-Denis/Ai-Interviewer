from domain.entities import Answer
from domain.enums import InterviewStatus

from application.repository_interfaces import AnswerRepository, InterviewRepository, QuestionRepository
from application.dtos import CreateAnswerDTO
from application.exceptions import (
    InterviewNotFoundException,
    QuestionNotFoundException,
    InterviewAlreadyCompletedException,
    InvalidAnswerOrderException,
)


class SubmitAnswerUseCase:
    
    def __init__(
        self,
        answer_repository: AnswerRepository,
        interview_repository: InterviewRepository,
        question_repository: QuestionRepository,
    ):
        self.answer_repository = answer_repository
        self.interview_repository = interview_repository
        self.question_repository = question_repository
    
    async def execute(self, dto: CreateAnswerDTO) -> Answer:
        interview = await self.interview_repository.get_by_id(dto.interview_id)
        if not interview:
            raise InterviewNotFoundException(dto.interview_id)
        
        if interview.status == InterviewStatus.COMPLETED:
            raise InterviewAlreadyCompletedException(dto.interview_id)
        
        question = await self.question_repository.get_by_id(dto.question_id)
        if not question:
            raise QuestionNotFoundException(dto.question_id)
        
        if question.interview_id != dto.interview_id:
            raise InvalidAnswerOrderException(
                f"Question {dto.question_id} does not belong to interview {dto.interview_id}"
            )
        
        existing_answers = await self.answer_repository.get_by_interview_id(dto.interview_id)
        existing_question_ids = {answer.question_id for answer in existing_answers}
        
        all_questions = await self.question_repository.get_by_interview_id(dto.interview_id)
        sorted_questions = sorted(all_questions, key=lambda question: question.question_order)
        
        current_question_order = next(
            (question.question_order for question in sorted_questions if question.question_id == dto.question_id),
            None
        )
        
        if current_question_order is None:
            raise InvalidAnswerOrderException(
                f"Question {dto.question_id} not found in interview {dto.interview_id}"
            )
        
        for question in sorted_questions:
            if question.question_order < current_question_order and question.question_id not in existing_question_ids:
                raise InvalidAnswerOrderException(
                    f"Cannot submit answer for question {dto.question_id} (order {current_question_order}). "
                    f"Please answer question {question.question_id} (order {question.question_order}) first."
                )
        
        existing_answers_for_question = await self.answer_repository.get_by_question_id(dto.question_id)
        if existing_answers_for_question:
            raise InvalidAnswerOrderException(
                f"Answer already exists for question {dto.question_id}"
            )
        
        if interview.status == InterviewStatus.NOT_STARTED:
            interview.start()
        
        interview.touch()
        await self.interview_repository.update(interview)
        
        answer = Answer(
            text=dto.text,
            question_id=dto.question_id,
            interview_id=dto.interview_id,
        )
        return await self.answer_repository.create(answer)
