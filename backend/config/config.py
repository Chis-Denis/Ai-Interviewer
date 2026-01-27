from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


def load_yaml_config() -> Dict[str, Any]:
    config_path = Path(__file__).parent / "default.yaml"
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    return {}


_yaml_config = load_yaml_config()


class Settings(BaseSettings):
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    CORS_ORIGINS: List[str] = []
    
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = _yaml_config.get("llm", {}).get("base_url", "https://api.openai.com/v1")
    LLM_MODEL: str = ""
    LLM_TEMPERATURE: float = _yaml_config.get("llm", {}).get("temperature", 0.7)
    LLM_MAX_TOKENS: int = _yaml_config.get("llm", {}).get("max_tokens", 2000)
    
    MAX_QUESTIONS_PER_INTERVIEW: int = _yaml_config.get("interview", {}).get("max_questions", 5)
    PROMPT_VERSION: str = _yaml_config.get("prompts", {}).get("version", "v1")
    PROMPT_TEMPLATES_PATH: str = _yaml_config.get("prompts", {}).get("templates_path", "")


settings = Settings()
