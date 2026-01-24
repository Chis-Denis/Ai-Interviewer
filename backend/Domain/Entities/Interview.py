from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from Domain.Enums.InterviewStatus import InterviewStatus


class Interview:
    
    def __init__(
        self,
        topic: str,
        interview_id: Optional[UUID] = None,
        status: InterviewStatus = InterviewStatus.NOT_STARTED,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ):
        self.interview_id = interview_id or uuid4()
        self.topic = topic
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.completed_at = completed_at
    
    def start(self) -> None:
        if self.status == InterviewStatus.NOT_STARTED:
            self.status = InterviewStatus.IN_PROGRESS
            self.updated_at = datetime.utcnow()
    
    def complete(self) -> None:
        if self.status == InterviewStatus.IN_PROGRESS:
            self.status = InterviewStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
    
    def cancel(self) -> None:
        self.status = InterviewStatus.CANCELLED
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"<Interview(id={self.interview_id}, topic='{self.topic}', status={self.status.value})>"
