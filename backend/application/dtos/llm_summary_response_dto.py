from typing import List
from pydantic import BaseModel, Field

from domain.enums import SentimentLabel


class LlmSummaryResponseDTO(BaseModel):
    themes: List[str] = Field(..., min_length=1)
    key_points: List[str] = Field(..., min_length=1)
    sentiment_score: float = Field(..., ge=0.0, le=1.0)
    sentiment_label: SentimentLabel
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    full_summary_text: str
