from typing import List, Optional, Dict, Any
from uuid import UUID

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)

from Application.Services import LlmService
from Application.Services.llm_data import QuestionData, AnswerData
from Application.Exceptions import LlmServiceError
from Infrastructure.LLM.prompt_builder import PromptBuilder
from Infrastructure.LLM.response_parser import ResponseParser


class OpenAIService(LlmService):
    
    def __init__(self, settings: "Settings"):
        self.settings = settings
        self.api_key = settings.LLM_API_KEY.strip() if settings.LLM_API_KEY else ""
        self.base_url = "https://api.openai.com/v1"
        self.timeout = 30.0
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def generate_question(
        self,
        topic: str,
        interview_id: UUID,
        existing_questions: Optional[List[QuestionData]] = None,
        previous_answers: Optional[List[AnswerData]] = None,
    ) -> str:
        if not self.api_key:
            raise LlmServiceError("LLM API key not configured")
        
        context = PromptBuilder.build_question_context(topic, existing_questions, previous_answers)
        prompt = PromptBuilder.build_question_prompt(context)
        
        try:
            response = await self._call_openai_api(prompt)
            return response.strip()
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_msg = f"OpenAI API error: {status_code}"
            if e.response.text:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('error', {}).get('message', e.response.text)}"
                except (ValueError, KeyError):
                    error_msg += f" - {e.response.text[:200]}"
            raise LlmServiceError(error_msg)
        except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPError) as e:
            raise LlmServiceError(f"Network error: {str(e)}")
    
    async def generate_summary(
        self,
        interview_topic: str,
        answers: List[AnswerData],
        questions: List[QuestionData],
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise LlmServiceError("LLM API key not configured")
        
        if not answers:
            raise LlmServiceError("Cannot generate summary without answers")
        
        prompt = PromptBuilder.build_summary_prompt(interview_topic, questions, answers)
        try:
            response_text = await self._call_openai_api(prompt)
            return ResponseParser.parse_summary_response(response_text)
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_msg = f"OpenAI API error: {status_code}"
            if e.response.text:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('error', {}).get('message', e.response.text)}"
                except (ValueError, KeyError):
                    error_msg += f" - {e.response.text[:200]}"
            raise LlmServiceError(error_msg)
        except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPError) as e:
            raise LlmServiceError(f"Network error: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        retry=retry_if_exception(lambda e: (
            isinstance(e, httpx.TimeoutException) or
            isinstance(e, (httpx.RequestError, httpx.HTTPError)) or
            (isinstance(e, httpx.HTTPStatusError) and e.response.status_code in [429, 500, 502, 503, 504])
        )),
        reraise=True,
    )
    async def _call_openai_api(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.settings.LLM_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.settings.LLM_TEMPERATURE,
            "max_tokens": self.settings.LLM_MAX_TOKENS,
        }
        
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
