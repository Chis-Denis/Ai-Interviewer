from typing import List
from pydantic import BaseModel, field_validator

from Domain.Enums import SentimentLabel
from Application.Exceptions import ValidationException


class SummaryResponseDTO(BaseModel):
    themes: List[str]
    key_points: List[str]
    sentiment_score: float
    sentiment_label: SentimentLabel
    confidence_score: float
    clarity_score: float
    strengths: List[str]
    weaknesses: List[str]
    consistency_score: float
    full_summary_text: str
    
    @field_validator('sentiment_score')
    @classmethod
    def validate_sentiment_score(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValidationException("sentiment_score must be between 0.0 and 1.0")
        return v
    
    @field_validator('confidence_score')
    @classmethod
    def validate_confidence_score(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValidationException("confidence_score must be between 0.0 and 1.0")
        return v
    
    @field_validator('clarity_score')
    @classmethod
    def validate_clarity_score(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValidationException("clarity_score must be between 0.0 and 1.0")
        return v
    
    @field_validator('consistency_score')
    @classmethod
    def validate_consistency_score(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValidationException("consistency_score must be between 0.0 and 1.0")
        return v
    
    @field_validator('themes')
    @classmethod
    def validate_themes(cls, v: List[str]) -> List[str]:
        if not v or len(v) == 0:
            raise ValidationException("themes cannot be empty")
        return v
    
    @field_validator('key_points')
    @classmethod
    def validate_key_points(cls, v: List[str]) -> List[str]:
        if not v or len(v) == 0:
            raise ValidationException("key_points cannot be empty")
        return v
    
    @field_validator('strengths')
    @classmethod
    def validate_strengths(cls, v: List[str]) -> List[str]:
        if not v or len(v) == 0:
            raise ValidationException("strengths cannot be empty")
        return v
    
    @field_validator('weaknesses')
    @classmethod
    def validate_weaknesses(cls, v: List[str]) -> List[str]:
        if not v or len(v) == 0:
            raise ValidationException("weaknesses cannot be empty")
        return v