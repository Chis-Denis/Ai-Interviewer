from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from Application.UseCases import GenerateSummaryUseCase, GetSummaryUseCase
from Application.dtos import InterviewSummaryResponseDTO
from Presentation.Mapping import interview_summary_to_response_dto
from Composition import (
    get_generate_summary_use_case,
    get_summary_use_case,
)


router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.post("/interview/{interview_id}", response_model=InterviewSummaryResponseDTO)
async def generate_summary(
    interview_id: UUID,
    use_case: GenerateSummaryUseCase = Depends(get_generate_summary_use_case),
):
    try:
        summary = await use_case.execute(interview_id)
        return interview_summary_to_response_dto(summary)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/interview/{interview_id}", response_model=InterviewSummaryResponseDTO)
async def get_summary(
    interview_id: UUID,
    use_case: GetSummaryUseCase = Depends(get_summary_use_case),
):
    summary = await use_case.execute(interview_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found for this interview")
    return interview_summary_to_response_dto(summary)
