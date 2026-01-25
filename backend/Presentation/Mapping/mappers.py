from Domain.Entities import Interview, Question, Answer, InterviewSummary
from Application.dtos import InterviewResponseDTO, QuestionResponseDTO, AnswerResponseDTO, InterviewSummaryResponseDTO


def interview_to_response_dto(interview: Interview) -> InterviewResponseDTO:
    return InterviewResponseDTO(
        interview_id=interview.interview_id,
        topic=interview.topic,
        status=interview.status.value,
        created_at=interview.created_at,
        updated_at=interview.updated_at,
        completed_at=interview.completed_at,
    )


def question_to_response_dto(question: Question) -> QuestionResponseDTO:
    return QuestionResponseDTO(
        question_id=question.question_id,
        text=question.text,
        interview_id=question.interview_id,
        question_order=question.question_order,
        created_at=question.created_at,
    )


def answer_to_response_dto(answer: Answer) -> AnswerResponseDTO:
    return AnswerResponseDTO(
        answer_id=answer.answer_id,
        text=answer.text,
        question_id=answer.question_id,
        interview_id=answer.interview_id,
        created_at=answer.created_at,
    )


def interview_summary_to_response_dto(summary: InterviewSummary) -> InterviewSummaryResponseDTO:
    return InterviewSummaryResponseDTO(
        summary_id=summary.summary_id,
        interview_id=summary.interview_id,
        themes=summary.themes,
        key_points=summary.key_points,
        strengths=summary.strengths,
        weaknesses=summary.weaknesses,
        missing_information=summary.missing_information,
        sentiment_score=summary.sentiment_score,
        sentiment_label=summary.sentiment_label,
        confidence_score=summary.confidence_score,
        clarity_score=summary.clarity_score,
        consistency_score=summary.consistency_score,
        overall_usefulness=summary.overall_usefulness,
        full_summary_text=summary.full_summary_text,
        created_at=summary.created_at,
    )
