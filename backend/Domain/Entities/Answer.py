from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Answer:
    
    def __init__(
        self,
        text: str,
        question_id: UUID,
        interview_id: UUID,
        answer_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.answer_id = answer_id or uuid4()
        self.text = text
        self.question_id = question_id
        self.interview_id = interview_id
        self.created_at = created_at or datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"<Answer(id={self.answer_id}, text='{self.text[:50]}...')>"
