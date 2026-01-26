from typing import List
from Application.Services.llm_data import AnswerData
from Application.Analysis.AnswerMetrics import AnswerMetrics


class AnswerEvaluator:
    
    @staticmethod
    def calculate_clarity_score(text: str) -> float:
        word_count = AnswerMetrics.calculate_word_count(text)
        sentence_count = AnswerMetrics.calculate_sentence_count(text)
        has_structure = AnswerMetrics.has_structure_indicators(text)
        
        if word_count < 5:
            return 0.1
        elif word_count < 10:
            return 0.3
        
        score = 0.5
        
        if sentence_count >= 2:
            score += 0.2
        
        if has_structure:
            score += 0.2
        
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        if 10 <= avg_words_per_sentence <= 25:
            score += 0.1
        
        return min(score, 1.0)
    
    @staticmethod
    def calculate_confidence_score(text: str) -> float:
        word_count = AnswerMetrics.calculate_word_count(text)
        completeness = AnswerMetrics.calculate_completeness_score(text)
        has_examples = AnswerMetrics.has_examples(text)
        has_metrics = AnswerMetrics.has_metrics_or_numbers(text)
        
        score = completeness * 0.5
        
        if word_count >= 50:
            score += 0.2
        elif word_count >= 30:
            score += 0.1
        
        if has_examples:
            score += 0.15
        
        if has_metrics:
            score += 0.15
        
        return min(score, 1.0)
    
    @staticmethod
    def evaluate_all_answers(answers: List[AnswerData]) -> dict:
        if not answers:
            return {
                'clarity_score': 0.0,
                'confidence_score': 0.0,
            }
        
        clarity_scores = [AnswerEvaluator.calculate_clarity_score(a.text) for a in answers]
        confidence_scores = [AnswerEvaluator.calculate_confidence_score(a.text) for a in answers]
        
        avg_clarity = sum(clarity_scores) / len(clarity_scores)
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        return {
            'clarity_score': round(avg_clarity, 2),
            'confidence_score': round(avg_confidence, 2),
        }
