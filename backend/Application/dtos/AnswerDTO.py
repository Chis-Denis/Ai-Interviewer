from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, field_serializer


class CreateAnswerDTO(BaseModel):
    text: str
    question_id: UUID
    interview_id: UUID


class AnswerResponseDTO(BaseModel):
    answer_id: UUID
    text: str
    question_id: UUID
    interview_id: UUID
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        local_time = value.astimezone()
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True
