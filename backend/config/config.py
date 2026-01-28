from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


def load_yaml_config() -> Dict[str, Any]:
    config_path = Path(__file__).parent / "default.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f) or {}


_yaml_config = load_yaml_config()


class Settings(BaseSettings):
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    CORS_ORIGINS: List[str] = _yaml_config["cors"]["origins"]
    
    LLM_API_KEY: str
    LLM_BASE_URL: str = _yaml_config["llm"]["base_url"]
    LLM_MODEL: str
    LLM_TEMPERATURE: float = _yaml_config["llm"]["temperature"]
    LLM_MAX_TOKENS: int = _yaml_config["llm"]["max_tokens"]
    
    MAX_QUESTIONS_PER_INTERVIEW: int = _yaml_config["interview"]["max_questions"]
    PROMPT_VERSION: str = _yaml_config["prompts"]["version"]
    PROMPT_TEMPLATES_PATH: str = _yaml_config["prompts"]["templates_path"]


settings = Settings()
