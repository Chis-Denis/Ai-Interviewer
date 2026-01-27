from uuid import UUID

from domain.entities import Question
from application.repository_interfaces import QuestionRepository
from application.exceptions import QuestionNotFoundException
from application.use_cases.base_use_case import BaseGetWithInterviewIdUseCase


class GetQuestionUseCase(BaseGetWithInterviewIdUseCase[Question, QuestionRepository]):
    
    def _create_not_found_exception(self, entity_id: UUID) -> Exception:
        return QuestionNotFoundException(entity_id)
