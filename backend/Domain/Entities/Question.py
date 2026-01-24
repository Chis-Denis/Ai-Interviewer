from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4


class Question:
    
    def __init__(
        self,
        text: str,
        interview_id: UUID,
        question_id: Optional[UUID] = None,
        question_order: int = 1,
        created_at: Optional[datetime] = None,
    ):
        self.question_id = question_id or uuid4()
        self.text = text
        self.interview_id = interview_id
        self.question_order = question_order
        self.created_at = created_at or datetime.now(timezone.utc)
    
    def __repr__(self) -> str:
        return f"<Question(id={self.question_id}, order={self.question_order}, text='{self.text[:50]}...')>"
