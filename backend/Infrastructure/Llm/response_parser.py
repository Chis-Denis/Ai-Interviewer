import json
from typing import Dict, Any
from Application.Exceptions import ValidationException


class ResponseParser:
    
    @staticmethod
    def parse_summary_response(response_text: str) -> Dict[str, Any]:
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
            
            sentiment_score = summary_data.get("sentiment_score")
            if sentiment_score is None:
                sentiment_score = 0
            else:
                sentiment_score = float(sentiment_score)
            
            strengths = summary_data.get("strengths")
            if strengths is None:
                strengths = []
            
            weaknesses = summary_data.get("weaknesses")
            if weaknesses is None:
                weaknesses = []
            
            missing_information = summary_data.get("missing_information")
            if missing_information is None:
                missing_information = []
            
            return {
                "themes": summary_data.get("themes", []),
                "key_points": summary_data.get("key_points", []),
                "sentiment_score": sentiment_score,
                "sentiment_label": summary_data.get("sentiment_label", "neutral"),
                "strengths": strengths,
                "weaknesses": weaknesses,
                "missing_information": missing_information,
                "full_summary_text": summary_data.get("full_summary_text", ""),
            }
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValidationException(f"Failed to parse summary response: {str(e)}")
