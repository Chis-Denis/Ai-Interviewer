import re
from typing import List

from Application.Services.llm_data import AnswerData


class AnswerMetrics:
    
    @staticmethod
    def calculate_word_count(text: str) -> int:
        return len(text.split())
    
    @staticmethod
    def calculate_sentence_count(text: str) -> int:
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        return len([s for s in sentences if s.strip()])
    
    @staticmethod
    def _contains_keywords(text: str, keywords: List[str]) -> bool:
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    @staticmethod
    def has_structure_indicators(text: str) -> bool:
        structure_keywords = ['because', 'since', 'when', 'if', 'then', 'therefore', 'however', 'although', 'first', 'second', 'finally', 'in addition', 'furthermore', 'moreover']
        return AnswerMetrics._contains_keywords(text, structure_keywords)
    
    @staticmethod
    def has_examples(text: str) -> bool:
        example_keywords = ['example', 'instance', 'case', 'such as', 'for instance', 'like', 'e.g.', 'including']
        return AnswerMetrics._contains_keywords(text, example_keywords)
    
    @staticmethod
    def has_metrics_or_numbers(text: str) -> bool:
        numbers = re.findall(r'\d+', text)
        metric_keywords = ['percent', '%', 'times', 'x', 'increase', 'decrease', 'rate', 'ratio']
        return len(numbers) > 0 or AnswerMetrics._contains_keywords(text, metric_keywords)
    
    @staticmethod
    def calculate_completeness_score(text: str) -> float:
        word_count = AnswerMetrics.calculate_word_count(text)
        return min(1.0, word_count / 100.0)
