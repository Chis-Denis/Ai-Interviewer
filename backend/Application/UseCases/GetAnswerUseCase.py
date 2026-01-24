from typing import List
from uuid import UUID
from Domain.Entities import Answer
from Application.RepositoryInterfaces import AnswerRepository
from Application.Exceptions import AnswerNotFoundException


class GetAnswerUseCase:
    
    def __init__(self, answer_repository: AnswerRepository):
        self.answer_repository = answer_repository
    
    async def execute(self, answer_id: UUID) -> Answer:
        answer = await self.answer_repository.get_by_id(answer_id)
        if not answer:
            raise AnswerNotFoundException(str(answer_id))
        return answer
    
    async def execute_by_interview_id(self, interview_id: UUID) -> List[Answer]:
        return await self.answer_repository.get_by_interview_id(interview_id)
    
    async def execute_by_question_id(self, question_id: UUID) -> List[Answer]:
        return await self.answer_repository.get_by_question_id(question_id)
