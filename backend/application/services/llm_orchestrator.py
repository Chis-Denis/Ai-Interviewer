from typing import List, Optional, Dict, Any
from uuid import UUID

from application.services.llm_client import LLMClient
from application.services.prompt_builder import PromptBuilder
from application.services.response_parser import ResponseParser
from application.services.llm_data import QuestionData, AnswerData
from application.exceptions import LlmServiceError, ValidationException


class LLMOrchestrator:
    
    def __init__(
        self,
        llm_client: LLMClient,
        prompt_builder: Optional[PromptBuilder] = None,
        response_parser: Optional[ResponseParser] = None,
    ):
        self.llm_client = llm_client
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.response_parser = response_parser or ResponseParser()
    
    async def generate_question(
        self,
        topic: str,
        interview_id: UUID,
        existing_questions: Optional[List[QuestionData]] = None,
        previous_answers: Optional[List[AnswerData]] = None,
    ) -> str:
        try:
            context = self.prompt_builder.build_question_context(
                topic, existing_questions, previous_answers
            )
            prompt = self.prompt_builder.build_question_prompt(context)
            
            response = await self.llm_client.call(prompt)
            return response.strip()
        except Exception as e:
            if isinstance(e, LlmServiceError):
                raise
            raise LlmServiceError(f"Failed to generate question: {str(e)}") from e
    
    async def generate_summary(
        self,
        interview_topic: str,
        answers: List[AnswerData],
        questions: List[QuestionData],
    ) -> Dict[str, Any]:
        if not answers:
            raise LlmServiceError("Cannot generate summary without answers")
        
        try:
            prompt = self.prompt_builder.build_summary_prompt(
                interview_topic, questions, answers
            )
            
            response_text = await self.llm_client.call(prompt)
            return self.response_parser.parse_summary_response(response_text)
        except Exception as e:
            if isinstance(e, (LlmServiceError, ValidationException)):
                raise
            raise LlmServiceError(f"Failed to generate summary: {str(e)}") from e
