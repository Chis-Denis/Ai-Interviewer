from Domain.Entities import Answer
from Application.RepositoryInterfaces import AnswerRepository
from Application.dtos import CreateAnswerDTO


class SubmitAnswerUseCase:
    
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository
    
    async def execute(self, dto: CreateAnswerDTO) -> Answer:
        answer = Answer(
            text=dto.text,
            question_id=dto.question_id,
            interview_id=dto.interview_id,
        )
        return await self.answer_repository.create(answer)
