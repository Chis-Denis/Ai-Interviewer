from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from Application.UseCases import GenerateQuestionUseCase, GetQuestionUseCase
from Application.dtos import GenerateQuestionDTO, QuestionResponseDTO
from Presentation.Mapping import question_to_response_dto
from Composition import (
    get_generate_question_use_case,
    get_question_use_case,
)


router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=QuestionResponseDTO)
async def generate_question(
    dto: GenerateQuestionDTO,
    use_case: GenerateQuestionUseCase = Depends(get_generate_question_use_case),
):
    try:
        question = await use_case.execute(dto)
        return question_to_response_dto(question)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{question_id}", response_model=QuestionResponseDTO)
async def get_question(
    question_id: UUID,
    use_case: GetQuestionUseCase = Depends(get_question_use_case),
):
    question = await use_case.execute(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question_to_response_dto(question)


@router.get("/interview/{interview_id}", response_model=List[QuestionResponseDTO])
async def get_questions_by_interview(
    interview_id: UUID,
    use_case: GetQuestionUseCase = Depends(get_question_use_case),
):
    questions = await use_case.execute_by_interview_id(interview_id)
    return [question_to_response_dto(question) for question in questions]
