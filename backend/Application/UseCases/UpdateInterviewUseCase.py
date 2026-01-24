from uuid import UUID
from Domain.Entities import Interview
from Application.RepositoryInterfaces import InterviewRepository
from Application.dtos import UpdateInterviewDTO
from Application.Exceptions import InterviewNotFoundException
from Domain.Enums import InterviewStatus


class UpdateInterviewUseCase:
    
    def __init__(self, interview_repository: InterviewRepository):
        self.interview_repository = interview_repository
    
    async def execute(self, interview_id: UUID, dto: UpdateInterviewDTO) -> Interview:
        interview = await self.interview_repository.get_by_id(interview_id)
        if not interview:
            raise InterviewNotFoundException(str(interview_id))
        
        if dto.topic is not None:
            interview.topic = dto.topic
        
        if dto.status is not None:
            if dto.status == InterviewStatus.IN_PROGRESS:
                interview.start()
            elif dto.status == InterviewStatus.COMPLETED:
                interview.complete()
            elif dto.status == InterviewStatus.CANCELLED:
                interview.cancel()
        
        return await self.interview_repository.update(interview)
