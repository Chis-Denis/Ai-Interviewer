from Domain.Entities import Question
from Application.RepositoryInterfaces import QuestionRepository, InterviewRepository
from Application.dtos import GenerateQuestionDTO


class GenerateQuestionUseCase:
    
    def __init__(
        self,
        question_repository: QuestionRepository,
        interview_repository: InterviewRepository,
    ):
        self.question_repository = question_repository
        self.interview_repository = interview_repository
    
    async def execute(self, dto: GenerateQuestionDTO) -> Question:
        pass
