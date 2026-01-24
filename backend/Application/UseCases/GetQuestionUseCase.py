from typing import List
from uuid import UUID

from Domain.Entities import Question

from Application.RepositoryInterfaces import QuestionRepository
from Application.Exceptions import QuestionNotFoundException


class GetQuestionUseCase:
    
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository
    
    async def execute(self, question_id: UUID) -> Question:
        question = await self.question_repository.get_by_id(question_id)
        if not question:
            raise QuestionNotFoundException(question_id)
        return question
    
    async def execute_by_interview_id(self, interview_id: UUID) -> List[Question]:
        return await self.question_repository.get_by_interview_id(interview_id)
