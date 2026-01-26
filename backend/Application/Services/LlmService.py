from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from Application.Services.llm_data import QuestionData, AnswerData


class LlmService(ABC):
    
    @abstractmethod
    async def generate_question(
        self,
        topic: str,
        interview_id: UUID,
        existing_questions: Optional[List[QuestionData]] = None,
        previous_answers: Optional[List[AnswerData]] = None,
    ) -> str:
        pass
    
    @abstractmethod
    async def generate_summary(
        self,
        interview_topic: str,
        answers: List[AnswerData],
        questions: List[QuestionData],
    ) -> Dict[str, Any]:
        pass
