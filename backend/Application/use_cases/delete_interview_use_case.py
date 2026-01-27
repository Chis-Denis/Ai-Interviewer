from uuid import UUID

from domain.entities import Interview
from application.repository_interfaces import InterviewRepository
from application.exceptions import InterviewNotFoundException
from application.use_cases.base_use_case import BaseDeleteUseCase


class DeleteInterviewUseCase(BaseDeleteUseCase[Interview, InterviewRepository]):
    
    def _create_not_found_exception(self, entity_id: UUID) -> Exception:
        return InterviewNotFoundException(entity_id)
