from uuid import UUID
from typing import Optional
from Domain.Entities import Interview, Question, Answer, InterviewSummary
from Infrastructure.Db.models import (
    InterviewModel,
    QuestionModel,
    AnswerModel,
    InterviewSummaryModel,
)
from Domain.Enums import InterviewStatus


def interview_model_to_entity(model: InterviewModel) -> Interview:
    return Interview(
        topic=model.topic,
        interview_id=UUID(model.interview_id),
        status=InterviewStatus(model.status),
        created_at=model.created_at,
        updated_at=model.updated_at,
        completed_at=model.completed_at,
    )


def interview_entity_to_model(entity: Interview) -> InterviewModel:
    return InterviewModel(
        interview_id=str(entity.interview_id),
        topic=entity.topic,
        status=entity.status.value,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        completed_at=entity.completed_at,
    )


def question_model_to_entity(model: QuestionModel) -> Question:
    return Question(
        text=model.text,
        interview_id=UUID(model.interview_id),
        question_id=UUID(model.question_id),
        question_order=model.question_order,
        created_at=model.created_at,
    )


def question_entity_to_model(entity: Question) -> QuestionModel:
    return QuestionModel(
        question_id=str(entity.question_id),
        text=entity.text,
        interview_id=str(entity.interview_id),
        question_order=entity.question_order,
        created_at=entity.created_at,
    )


def answer_model_to_entity(model: AnswerModel) -> Answer:
    return Answer(
        text=model.text,
        question_id=UUID(model.question_id),
        interview_id=UUID(model.interview_id),
        answer_id=UUID(model.answer_id),
        created_at=model.created_at,
    )


def answer_entity_to_model(entity: Answer) -> AnswerModel:
    return AnswerModel(
        answer_id=str(entity.answer_id),
        text=entity.text,
        question_id=str(entity.question_id),
        interview_id=str(entity.interview_id),
        created_at=entity.created_at,
    )


def interview_summary_model_to_entity(model: InterviewSummaryModel) -> InterviewSummary:
    return InterviewSummary(
        interview_id=UUID(model.interview_id),
        themes=model.themes if model.themes else [],
        key_points=model.key_points if model.key_points else [],
        summary_id=UUID(model.summary_id),
        sentiment_score=model.sentiment_score,
        sentiment_label=model.sentiment_label,
        full_summary_text=model.full_summary_text,
        created_at=model.created_at,
    )


def interview_summary_entity_to_model(entity: InterviewSummary) -> InterviewSummaryModel:
    return InterviewSummaryModel(
        summary_id=str(entity.summary_id),
        interview_id=str(entity.interview_id),
        themes=entity.themes,
        key_points=entity.key_points,
        sentiment_score=entity.sentiment_score,
        sentiment_label=entity.sentiment_label,
        full_summary_text=entity.full_summary_text,
        created_at=entity.created_at,
    )
