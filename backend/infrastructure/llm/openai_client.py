import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)

from application.services.llm_client import LLMClient
from application.exceptions import LlmServiceError
from application.services.service_constants import ServiceConstants
from config.config import Settings


class OpenAIClient(LLMClient):
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key = settings.LLM_API_KEY.strip() if settings.LLM_API_KEY else ""
        self.base_url = settings.LLM_BASE_URL
        self.timeout = ServiceConstants.LLMClient.DEFAULT_TIMEOUT_SECONDS
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def call(self, prompt: str) -> str:
        if not self.api_key:
            raise LlmServiceError("LLM API key not configured")
        
        try:
            response = await self._call_openai_api(prompt)
            return response
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_msg = f"OpenAI API error: {status_code}"
            if e.response.text:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('error', {}).get('message', e.response.text)}"
                except (ValueError, KeyError):
                    truncate_length = ServiceConstants.LLMClient.ERROR_TEXT_TRUNCATE_LENGTH
                    error_msg += f" - {e.response.text[:truncate_length]}"
            raise LlmServiceError(error_msg)
        except (httpx.TimeoutException, httpx.RequestError, httpx.HTTPError) as e:
            raise LlmServiceError(f"Network error: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(ServiceConstants.LLMClient.MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(
            multiplier=ServiceConstants.LLMClient.RETRY_WAIT_MULTIPLIER,
            min=ServiceConstants.LLMClient.RETRY_WAIT_MIN_SECONDS,
            max=ServiceConstants.LLMClient.RETRY_WAIT_MAX_SECONDS
        ),
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
    
    async def close(self):
        await self.client.aclose()
