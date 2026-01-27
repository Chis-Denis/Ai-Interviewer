from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4
from domain.enums import InterviewStatus


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
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)
        self.completed_at = completed_at
    
    def start(self) -> None:
        if self.status == InterviewStatus.NOT_STARTED:
            self.status = InterviewStatus.IN_PROGRESS
            self.updated_at = datetime.now(timezone.utc)
    
    def complete(self) -> None:
        if self.status == InterviewStatus.IN_PROGRESS:
            self.status = InterviewStatus.COMPLETED
            self.completed_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)
    
    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
    
    def __repr__(self) -> str:
        return f"<Interview(id={self.interview_id}, topic='{self.topic}', status={self.status.value})>"
