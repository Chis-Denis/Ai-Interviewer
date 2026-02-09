from domain.entities import Question
from application.repository_interfaces import QuestionRepository
from application.use_cases.base_use_case import BaseGetByInterviewIdUseCase


class GetQuestionUseCase(BaseGetByInterviewIdUseCase[Question, QuestionRepository]):
    pass
