from uuid import UUID

from domain.entities import Answer
from application.repository_interfaces import AnswerRepository
from application.exceptions import AnswerNotFoundException
from application.use_cases.base_use_case import BaseGetWithInterviewIdUseCase


class GetAnswerUseCase(BaseGetWithInterviewIdUseCase[Answer, AnswerRepository]):
    
    def _create_not_found_exception(self, entity_id: UUID) -> Exception:
        return AnswerNotFoundException(entity_id)
