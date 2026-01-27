from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, field_serializer


class QuestionResponseDTO(BaseModel):
    question_id: UUID
    text: str
    interview_id: UUID
    question_order: int
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        local_time = value.astimezone()
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        from_attributes = True
