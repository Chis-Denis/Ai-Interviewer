from fastapi import Depends
from sqlalchemy.orm import Session
from Infrastructure.Db.database import get_db
from Application.RepositoryInterfaces import InterviewRepository, QuestionRepository, AnswerRepository, InterviewSummaryRepository
from Infrastructure.Repositories import SqlInterviewRepository, SqlQuestionRepository, SqlAnswerRepository, SqlInterviewSummaryRepository
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


def get_interview_repository(db: Session = Depends(get_db)) -> InterviewRepository:
    return SqlInterviewRepository(db)


def get_question_repository(db: Session = Depends(get_db)) -> QuestionRepository:
    return SqlQuestionRepository(db)


def get_answer_repository(db: Session = Depends(get_db)) -> AnswerRepository:
    return SqlAnswerRepository(db)


def get_summary_repository(db: Session = Depends(get_db)) -> InterviewSummaryRepository:
    return SqlInterviewSummaryRepository(db)


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
) -> GenerateQuestionUseCase:
    return GenerateQuestionUseCase(question_repository, interview_repository)


def get_question_use_case(
    repository: QuestionRepository = Depends(get_question_repository)
) -> GetQuestionUseCase:
    return GetQuestionUseCase(repository)


def get_submit_answer_use_case(
    repository: AnswerRepository = Depends(get_answer_repository)
) -> SubmitAnswerUseCase:
    return SubmitAnswerUseCase(repository)


def get_answer_use_case(
    repository: AnswerRepository = Depends(get_answer_repository)
) -> GetAnswerUseCase:
    return GetAnswerUseCase(repository)


def get_generate_summary_use_case(
    interview_repository: InterviewRepository = Depends(get_interview_repository),
    answer_repository: AnswerRepository = Depends(get_answer_repository),
    summary_repository: InterviewSummaryRepository = Depends(get_summary_repository),
) -> GenerateSummaryUseCase:
    return GenerateSummaryUseCase(interview_repository, answer_repository, summary_repository)


def get_summary_use_case(
    repository: InterviewSummaryRepository = Depends(get_summary_repository)
) -> GetSummaryUseCase:
    return GetSummaryUseCase(repository)
