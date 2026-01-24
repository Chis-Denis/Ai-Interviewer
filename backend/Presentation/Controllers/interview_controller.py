from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from Application.UseCases import (
    CreateInterviewUseCase,
    GetInterviewUseCase,
    DeleteInterviewUseCase,
)
from Application.dtos import (
    CreateInterviewDTO,
    InterviewResponseDTO,
)
from Presentation.Mapping import interview_to_response_dto
from Composition import (
    get_create_interview_use_case,
    get_interview_use_case,
    get_delete_interview_use_case,
)


router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/", response_model=InterviewResponseDTO)
async def create_interview(
    dto: CreateInterviewDTO,
    use_case: CreateInterviewUseCase = Depends(get_create_interview_use_case),
):
    interview = await use_case.execute(dto)
    return interview_to_response_dto(interview)


@router.get("/{interview_id}", response_model=InterviewResponseDTO)
async def get_interview(
    interview_id: UUID,
    use_case: GetInterviewUseCase = Depends(get_interview_use_case),
):
    interview = await use_case.execute(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview_to_response_dto(interview)


@router.get("/", response_model=List[InterviewResponseDTO])
async def get_all_interviews(
    use_case: GetInterviewUseCase = Depends(get_interview_use_case),
):
    interviews = await use_case.execute_all()
    return [interview_to_response_dto(interview) for interview in interviews]


@router.delete("/{interview_id}")
async def delete_interview(
    interview_id: UUID,
    use_case: DeleteInterviewUseCase = Depends(get_delete_interview_use_case),
):
    deleted = await use_case.execute(interview_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Interview not found")
    return {"message": "Interview deleted successfully"}
