from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from Domain.Entities import Question, Answer


class LlmService(ABC):
    """LLM service interface for generating questions and summaries."""
    
    @abstractmethod
    async def generate_question(
        self,
        topic: str,
        interview_id: UUID,
        existing_questions: Optional[List[Question]] = None,
        previous_answers: Optional[List[Answer]] = None,
    ) -> str:
        """Generates interview question based on topic and context."""
        pass
    
    @abstractmethod
    async def generate_summary(
        self,
        interview_topic: str,
        answers: List[Answer],
        questions: List[Question],
    ) -> dict:
        """
        Generates interview summary with themes, key points, and sentiment.
        
        Returns dict with: themes, key_points, sentiment_score, sentiment_label, full_summary_text.
        """
        pass
