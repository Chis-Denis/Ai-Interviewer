from pydantic import BaseModel


class CreateInterviewDTO(BaseModel):
    topic: str
