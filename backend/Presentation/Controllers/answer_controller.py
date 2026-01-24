from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from Application.UseCases import SubmitAnswerUseCase, GetAnswerUseCase
from Application.dtos import CreateAnswerDTO, AnswerResponseDTO
from Presentation.Mapping import answer_to_response_dto
from Presentation.Validations.error_schemas import ValidationErrorResponse
from Composition import (
    get_submit_answer_use_case,
    get_answer_use_case,
)


router = APIRouter(prefix="/answers", tags=["answers"])


@router.post(
    "/",
    response_model=AnswerResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
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
    "/{answer_id}",
    response_model=AnswerResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Answer not found"},
    }
)
async def get_answer(
    answer_id: UUID,
    use_case: GetAnswerUseCase = Depends(get_answer_use_case),
):
    answer = await use_case.execute(answer_id)
    return answer_to_response_dto(answer)


@router.get(
    "/interview/{interview_id}",
    response_model=List[AnswerResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_answers_by_interview(
    interview_id: UUID,
    use_case: GetAnswerUseCase = Depends(get_answer_use_case),
):
    answers = await use_case.execute_by_interview_id(interview_id)
    return [answer_to_response_dto(answer) for answer in answers]


@router.get(
    "/question/{question_id}",
    response_model=List[AnswerResponseDTO],
    status_code=status.HTTP_200_OK
)
async def get_answers_by_question(
    question_id: UUID,
    use_case: GetAnswerUseCase = Depends(get_answer_use_case),
):
    answers = await use_case.execute_by_question_id(question_id)
    return [answer_to_response_dto(answer) for answer in answers]
