from typing import List
from uuid import UUID

from domain.entities import Interview
from application.repository_interfaces import InterviewRepository
from application.exceptions import InterviewNotFoundException
from application.use_cases.base_use_case import BaseGetByIdUseCase


class GetInterviewUseCase(BaseGetByIdUseCase[Interview, InterviewRepository]):
    
    def _create_not_found_exception(self, entity_id: UUID) -> Exception:
        return InterviewNotFoundException(entity_id)
    
    async def execute_all(self) -> List[Interview]:
        return await self.repository.get_all()
