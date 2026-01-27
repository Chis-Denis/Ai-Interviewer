from uuid import UUID

from fastapi import APIRouter, Depends, status

from application.use_cases import GenerateSummaryUseCase, GetSummaryUseCase
from presentation.dtos import InterviewSummaryResponseDTO
from composition import (
    get_generate_summary_use_case,
    get_summary_use_case,
)
from presentation.mappers import interview_summary_to_response_dto

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.post(
    "/interview/{interview_id}",
    response_model=InterviewSummaryResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Interview not found"},
        400: {"description": "Business rule violation (no answers available)"},
    }
)
async def generate_summary(
    interview_id: UUID,
    use_case: GenerateSummaryUseCase = Depends(get_generate_summary_use_case),
):
    summary = await use_case.execute(interview_id)
    return interview_summary_to_response_dto(summary)


@router.get(
    "/interview/{interview_id}",
    response_model=InterviewSummaryResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Summary not found for this interview"},
    }
)
async def get_summary(
    interview_id: UUID,
    use_case: GetSummaryUseCase = Depends(get_summary_use_case),
):
    summary = await use_case.execute(interview_id)
    return interview_summary_to_response_dto(summary)
