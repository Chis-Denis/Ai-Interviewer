from fastapi import Depends
from sqlalchemy.orm import Session
from Infrastructure.Db.database import get_db
from Application.RepositoryInterfaces import InterviewRepository
from Infrastructure.Repositories import SqlInterviewRepository
from Application.UseCases import CreateInterviewUseCase, GetInterviewUseCase, DeleteInterviewUseCase


def get_interview_repository(db: Session = Depends(get_db)) -> InterviewRepository:
    return SqlInterviewRepository(db)


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
