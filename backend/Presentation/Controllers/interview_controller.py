from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from Application.UseCases import (
    CreateInterviewUseCase,
    GetInterviewUseCase,
)
from Application.dtos import (
    CreateInterviewDTO,
    InterviewResponseDTO,
)
from Presentation.Mapping import interview_to_response_dto
from Presentation.Dependencies import (
    get_create_interview_use_case,
    get_interview_use_case,
)


router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/", response_model=InterviewResponseDTO)
async def create_interview(
    dto: CreateInterviewDTO,
    use_case: CreateInterviewUseCase = Depends(get_create_interview_use_case),
):
    pass


@router.get("/{interview_id}", response_model=InterviewResponseDTO)
async def get_interview(
    interview_id: UUID,
    use_case: GetInterviewUseCase = Depends(get_interview_use_case),
):
    pass


@router.get("/", response_model=List[InterviewResponseDTO])
async def get_all_interviews(
    use_case: GetInterviewUseCase = Depends(get_interview_use_case),
):
    pass
