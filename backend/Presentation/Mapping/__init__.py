from Domain.Entities import Interview
from Application.dtos import InterviewResponseDTO


def interview_to_response_dto(interview: Interview) -> InterviewResponseDTO:
    return InterviewResponseDTO(
        interview_id=interview.interview_id,
        topic=interview.topic,
        status=interview.status.value,
        created_at=interview.created_at,
        updated_at=interview.updated_at,
        completed_at=interview.completed_at,
    )
