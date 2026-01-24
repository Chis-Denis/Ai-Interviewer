from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from Application.UseCases import GenerateQuestionUseCase, GetQuestionUseCase
from Application.dtos import GenerateQuestionDTO, QuestionResponseDTO
from Composition import (
    get_generate_question_use_case,
    get_question_use_case,
)
from Presentation.Mapping import question_to_response_dto
from Presentation.Validations.error_schemas import ValidationErrorResponse


router = APIRouter(prefix="/questions", tags=["questions"])


@router.post(
    "/",
    response_model=QuestionResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Interview not found"},
        400: {"description": "Business rule violation (interview completed, cancelled, or max questions reached)"},
        422: {"model": ValidationErrorResponse, "description": "Validation Error"},
    }
)
async def generate_question(
    dto: GenerateQuestionDTO,
    use_case: GenerateQuestionUseCase = Depends(get_generate_question_use_case),
):
    question = await use_case.execute(dto)
    return question_to_response_dto(question)


@router.get(
    "/{question_id}",
    response_model=QuestionResponseDTO,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Question not found"},
    }
)
async def get_question(
    question_id: UUID,
    use_case: GetQuestionUseCase = Depends(get_question_use_case),
):
    question = await use_case.execute(question_id)
    return question_to_response_dto(question)


@router.get(
    "/interview/{interview_id}",
    response_model=List[QuestionResponseDTO],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "List of questions for the interview"},
        404: {"description": "Interview not found"},
    }
)
async def get_questions_by_interview(
    interview_id: UUID,
    use_case: GetQuestionUseCase = Depends(get_question_use_case),
):
    questions = await use_case.execute_by_interview_id(interview_id)
    return [question_to_response_dto(question) for question in questions]
