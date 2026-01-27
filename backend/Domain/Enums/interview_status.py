from enum import Enum


class InterviewStatus(str, Enum):
    
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
