from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from Application.UseCases import SubmitAnswerUseCase, GetAnswerUseCase
from Application.DTOs import CreateAnswerDTO
from Presentation.DTOs import AnswerResponseDTO
from Composition import (
    get_submit_answer_use_case,
    get_answer_use_case,
)
from Presentation.Mappers import answer_to_response_dto
from Presentation.common import ValidationErrorResponse

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post(
    "/",
    response_model=AnswerResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Interview or question not found"},
        400: {"description": "Business rule violation (interview completed, cancelled, invalid answer order, or duplicate answer)"},
        422: {"model": ValidationErrorResponse, "description": "Validation Error"},
    }
)
async def submit_answer(
    dto: CreateAnswerDTO,
    use_case: SubmitAnswerUseCase = Depends(get_submit_answer_use_case),
):
    answer = await use_case.execute(dto)
    return answer_to_response_dto(answer)


@router.get(
    "/interview/{interview_id}",
    response_model=List[AnswerResponseDTO],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of answers for the interview"},
        404: {"description": "Interview not found"},
    }
)
async def get_answers_by_interview(
    interview_id: UUID,
    use_case: GetAnswerUseCase = Depends(get_answer_use_case),
):
    answers = await use_case.execute_by_interview_id(interview_id)
    return [answer_to_response_dto(answer) for answer in answers]
