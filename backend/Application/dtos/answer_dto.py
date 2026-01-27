from uuid import UUID
from pydantic import BaseModel


class CreateAnswerDTO(BaseModel):
    text: str
    question_id: UUID
    interview_id: UUID
