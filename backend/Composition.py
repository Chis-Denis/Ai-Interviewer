from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Infrastructure.Db.database import get_db
from Application.RepositoryInterfaces import InterviewRepository, QuestionRepository, AnswerRepository, InterviewSummaryRepository
from Infrastructure.Repositories import SqlInterviewRepository, SqlQuestionRepository, SqlAnswerRepository, SqlInterviewSummaryRepository
from Application.Service import LlmService
from Infrastructure.Llm import OpenAIService
from Core.config import settings


from Application.UseCases import (
    CreateInterviewUseCase,
    GetInterviewUseCase,
    DeleteInterviewUseCase,
    UpdateInterviewUseCase,
    GenerateQuestionUseCase,
    GetQuestionUseCase,
    SubmitAnswerUseCase,
    GetAnswerUseCase,
    GenerateSummaryUseCase,
    GetSummaryUseCase,
)


async def get_interview_repository(db: AsyncSession = Depends(get_db)) -> InterviewRepository:
    return SqlInterviewRepository(db)


async def get_question_repository(db: AsyncSession = Depends(get_db)) -> QuestionRepository:
    return SqlQuestionRepository(db)


async def get_answer_repository(db: AsyncSession = Depends(get_db)) -> AnswerRepository:
    return SqlAnswerRepository(db)


async def get_summary_repository(db: AsyncSession = Depends(get_db)) -> InterviewSummaryRepository:
    return SqlInterviewSummaryRepository(db)


def get_settings():
    """Provides settings configuration."""
    return settings


def get_llm_service(settings = Depends(get_settings)) -> LlmService:
    return OpenAIService(settings)


def get_create_interview_use_case(
    repository: InterviewRepository = Depends(get_interview_repository)
) -> CreateInterviewUseCase:
    return CreateInterviewUseCase(repository)


def get_interview_use_case(
    repository: InterviewRepository = Depends(get_interview_repository)
) -> GetInterviewUseCase:
    return GetInterviewUseCase(repository)


def get_delete_interview_use_case(
    repository: InterviewRepository = Depends(get_interview_repository)
) -> DeleteInterviewUseCase:
    return DeleteInterviewUseCase(repository)


def get_update_interview_use_case(
    repository: InterviewRepository = Depends(get_interview_repository)
) -> UpdateInterviewUseCase:
    return UpdateInterviewUseCase(repository)


def get_generate_question_use_case(
    question_repository: QuestionRepository = Depends(get_question_repository),
    interview_repository: InterviewRepository = Depends(get_interview_repository),
    answer_repository: AnswerRepository = Depends(get_answer_repository),
    llm_service: LlmService = Depends(get_llm_service),
    settings = Depends(get_settings),
) -> GenerateQuestionUseCase:
    return GenerateQuestionUseCase(question_repository, interview_repository, answer_repository, llm_service, settings)


def get_question_use_case(
    repository: QuestionRepository = Depends(get_question_repository)
) -> GetQuestionUseCase:
    return GetQuestionUseCase(repository)


def get_submit_answer_use_case(
    answer_repository: AnswerRepository = Depends(get_answer_repository),
    interview_repository: InterviewRepository = Depends(get_interview_repository),
    question_repository: QuestionRepository = Depends(get_question_repository),
) -> SubmitAnswerUseCase:
    return SubmitAnswerUseCase(answer_repository, interview_repository, question_repository)


def get_answer_use_case(
    repository: AnswerRepository = Depends(get_answer_repository)
) -> GetAnswerUseCase:
    return GetAnswerUseCase(repository)


def get_generate_summary_use_case(
    interview_repository: InterviewRepository = Depends(get_interview_repository),
    answer_repository: AnswerRepository = Depends(get_answer_repository),
    summary_repository: InterviewSummaryRepository = Depends(get_summary_repository),
    question_repository: QuestionRepository = Depends(get_question_repository),
    llm_service: LlmService = Depends(get_llm_service),
) -> GenerateSummaryUseCase:
    return GenerateSummaryUseCase(interview_repository, answer_repository, summary_repository, question_repository, llm_service)


def get_summary_use_case(
    repository: InterviewSummaryRepository = Depends(get_summary_repository)
) -> GetSummaryUseCase:
    return GetSummaryUseCase(repository)
