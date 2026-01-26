from uuid import UUID
from pydantic import BaseModel


class GenerateQuestionDTO(BaseModel):
    interview_id: UUID