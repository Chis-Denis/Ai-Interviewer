from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from uuid import UUID

T = TypeVar('T')
R = TypeVar('R')


class BaseUseCase(ABC, Generic[T, R]):
    
    def __init__(self, repository: R):
        self.repository = repository


class BaseGetByIdUseCase(BaseUseCase[T, R], ABC):
    
    @abstractmethod
    def _create_not_found_exception(self, entity_id: UUID) -> Exception:
        pass
    
    async def execute(self, entity_id: UUID) -> T:
        entity = await self.repository.get_by_id(entity_id)
        if not entity:
            raise self._create_not_found_exception(entity_id)
        return entity


class BaseGetByInterviewIdUseCase(BaseUseCase[T, R], ABC):
    
    async def execute_by_interview_id(self, interview_id: UUID) -> List[T]:
        return await self.repository.get_by_interview_id(interview_id)


class BaseDeleteUseCase(BaseUseCase[T, R], ABC):
    
    @abstractmethod
    def _create_not_found_exception(self, entity_id: UUID) -> Exception:
        pass
    
    async def execute(self, entity_id: UUID) -> None:
        deleted = await self.repository.delete(entity_id)
        if not deleted:
            raise self._create_not_found_exception(entity_id)
