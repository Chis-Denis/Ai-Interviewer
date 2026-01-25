from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    APP_NAME: str = "AI Interviewer"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"
    
    DATABASE_URL: str = ""
    DATABASE_ECHO: bool = False
    
    CORS_ORIGINS: List[str] = []
    
    LLM_API_KEY: str = ""
    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = ""
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000
    
    DEBUG: bool = False
    MAX_QUESTIONS_PER_INTERVIEW: int = 5


settings = Settings()
