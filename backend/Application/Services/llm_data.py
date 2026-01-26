from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID


@dataclass
class QuestionData:
    text: str
    question_order: int
    question_id: UUID


@dataclass
class AnswerData:
    text: str
    question_id: UUID