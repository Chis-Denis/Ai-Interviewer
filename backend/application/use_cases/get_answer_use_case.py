from domain.entities import Answer
from application.repository_interfaces import AnswerRepository
from application.use_cases.base_use_case import BaseGetByInterviewIdUseCase


class GetAnswerUseCase(BaseGetByInterviewIdUseCase[Answer, AnswerRepository]):
    pass
