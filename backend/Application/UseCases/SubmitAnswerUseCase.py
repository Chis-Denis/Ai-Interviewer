from Domain.Entities import Answer
from Application.RepositoryInterfaces import AnswerRepository
from Application.dtos import CreateAnswerDTO


class SubmitAnswerUseCase:
    
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository
    
    async def execute(self, dto: CreateAnswerDTO) -> Answer:
        pass
