from typing import List, Optional
from uuid import UUID
import json

import httpx
from Application.Service import LlmService
from Application.Exceptions import LlmServiceError
from Domain.Entities import Question, Answer


class OpenAIService(LlmService):
    
    def __init__(self, settings: "Settings"):
        self.api_key = settings.LLM_API_KEY.strip() if settings.LLM_API_KEY else ""
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.base_url = "https://api.openai.com/v1"
        self.timeout = 30.0
    
    async def generate_question(
        self,
        topic: str,
        interview_id: UUID,
        existing_questions: Optional[List[Question]] = None,
        previous_answers: Optional[List[Answer]] = None,
    ) -> str:
        if not self.api_key:
            raise LlmServiceError("LLM API key not configured")
        
        context = self._build_question_context(topic, existing_questions, previous_answers)
        prompt = self._build_question_prompt(context)
        
        response = await self._call_openai_api(prompt)
        return response.strip()
    
    async def generate_summary(
        self,
        interview_topic: str,
        answers: List[Answer],
        questions: List[Question],
    ) -> dict:
        if not self.api_key:
            raise LlmServiceError("LLM API key not configured")
        
        if not answers:
            raise LlmServiceError("Cannot generate summary without answers")
        
        prompt = self._build_summary_prompt(interview_topic, questions, answers)
        response_text = await self._call_openai_api(prompt)
        return self._parse_summary_response(response_text)
    
    def _build_question_context(
        self,
        topic: str,
        existing_questions: Optional[List[Question]],
        previous_answers: Optional[List[Answer]],
    ) -> str:
        context_parts = [f"Interview topic: {topic}"]
        
        if existing_questions:
            context_parts.append("\nPreviously asked questions:")
            for q in existing_questions:
                context_parts.append(f"- {q.text}")
        
        if previous_answers:
            context_parts.append("\nPrevious answers:")
            for a in previous_answers:
                context_parts.append(f"- {a.text}")
        
        return "\n".join(context_parts)
        
    

    def _build_question_prompt(self, context: str) -> str:

        return f"""You are an expert interviewer conducting a technical interview.

{context}

Generate a single, clear, and relevant interview question that:
- Is appropriate for the interview topic
- Builds on previous questions and answers if provided
- Is specific and actionable
- Helps assess the candidate's knowledge and experience

Return only the question text, without any additional explanation or formatting."""


    def _build_summary_prompt(
        self,
        topic: str,
        questions: List[Question],
        answers: List[Answer],
    ) -> str:
        """Builds the prompt for summary generation."""
        qa_pairs = []
        for q, a in zip(sorted(questions, key=lambda x: x.question_order), answers):
            qa_pairs.append(f"Q: {q.text}\nA: {a.text}")
        
        qa_text = "\n\n".join(qa_pairs)
        
        return f"""Analyze the following interview and provide a comprehensive summary.

Interview Topic: {topic}

Questions and Answers:
{qa_text}

Provide a JSON response with the following structure:
{{
    "themes": ["theme1", "theme2", "theme3"],
    "key_points": ["point1", "point2", "point3", "point4", "point5"],
    "sentiment_score": 0.75,
    "sentiment_label": "positive",
    "full_summary_text": "A detailed summary of the interview..."
}}

Requirements:
- themes: 3 main themes identified (list of strings)
- key_points: 5 key points extracted (list of strings)
- sentiment_score: Float between 0.0 and 1.0 (0.0=negative, 0.5=neutral, 1.0=positive)
- sentiment_label: One of "positive", "neutral", or "negative"
- full_summary_text: Complete summary paragraph (2-3 sentences)

Return only valid JSON, no additional text."""



    async def _call_openai_api(self, prompt: str) -> str:
        """Makes async API call to OpenAI."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            error_msg = f"OpenAI API error: {e.response.status_code}"
            if e.response.text:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('error', {}).get('message', e.response.text)}"
                except (ValueError, KeyError):
                    error_msg += f" - {e.response.text[:200]}"
            raise LlmServiceError(error_msg)
        except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException) as e:
            raise LlmServiceError(f"Network error: {str(e)}")
    
    def _parse_summary_response(self, response_text: str) -> dict:
        """Parses and validates summary response from LLM."""
        try:
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            summary_data = json.loads(cleaned_text)
            
            return {
                "themes": summary_data.get("themes", []),
                "key_points": summary_data.get("key_points", []),
                "sentiment_score": float(summary_data.get("sentiment_score", 0.5)),
                "sentiment_label": summary_data.get("sentiment_label", "neutral"),
                "full_summary_text": summary_data.get("full_summary_text", ""),
            }
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise LlmServiceError(f"Failed to parse summary response: {str(e)}")
