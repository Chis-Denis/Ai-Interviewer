from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from Application.UseCases import (
    CreateInterviewUseCase,
    GetInterviewUseCase,
    DeleteInterviewUseCase,
    UpdateInterviewUseCase,
)
from Application.DTOs import (
    CreateInterviewDTO,
    UpdateInterviewDTO,
)
from Presentation.DTOs import InterviewResponseDTO
from Composition import (
    get_create_interview_use_case,
    get_interview_use_case,
    get_delete_interview_use_case,
    get_update_interview_use_case,
)
from Presentation.Mappers import interview_to_response_dto
from Presentation.common import ValidationErrorResponse

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post(
    "/",
    response_model=InterviewResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        422: {"model": ValidationErrorResponse, "description": "Validation Error"},
    }
)
async def create_interview(
    dto: CreateInterviewDTO,
    use_case: CreateInterviewUseCase = Depends(get_create_interview_use_case),
):
    interview = await use_case.execute(dto)
    return interview_to_response_dto(interview)


@router.get(
    "/{interview_id}",
    response_model=InterviewResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Interview not found"},
    }
)
async def get_interview(
    interview_id: UUID,
    use_case: GetInterviewUseCase = Depends(get_interview_use_case),
):
    interview = await use_case.execute(interview_id)
    return interview_to_response_dto(interview)


@router.get(
    "/",
    response_model=List[InterviewResponseDTO],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of interviews"},
    }
)
async def get_all_interviews(
    use_case: GetInterviewUseCase = Depends(get_interview_use_case),
):
    interviews = await use_case.execute_all()
    return [interview_to_response_dto(interview) for interview in interviews]


@router.patch(
    "/{interview_id}",
    response_model=InterviewResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Interview not found"},
        400: {"description": "Business rule violation (interview already completed)"},
        422: {"model": ValidationErrorResponse, "description": "Validation Error"},
    }
)
async def update_interview(
    interview_id: UUID,
    dto: UpdateInterviewDTO,
    use_case: UpdateInterviewUseCase = Depends(get_update_interview_use_case),
):
    interview = await use_case.execute(interview_id, dto)
    return interview_to_response_dto(interview)


@router.delete(
    "/{interview_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Interview not found"},
    }
)
async def delete_interview(
    interview_id: UUID,
    use_case: DeleteInterviewUseCase = Depends(get_delete_interview_use_case),
):
    await use_case.execute(interview_id)
    return None
