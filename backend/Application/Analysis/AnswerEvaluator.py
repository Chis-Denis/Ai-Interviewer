from typing import List
from Application.Services.llm_data import AnswerData
from Application.Analysis.AnswerMetrics import AnswerMetrics


class AnswerEvaluator:
    
    @staticmethod
    def calculate_clarity_score(text: str) -> float:
        if AnswerMetrics.detect_manipulation_attempts(text):
            return 0.0
        
        if AnswerMetrics.detect_gibberish(text):
            return 0.0
        
        word_count = AnswerMetrics.calculate_word_count(text)
        sentence_count = AnswerMetrics.calculate_sentence_count(text)
        has_structure = AnswerMetrics.has_structure_indicators(text)
        
        if word_count < 5:
            return 0.02
        elif word_count < 10:
            return 0.08
        elif word_count < 15:
            return 0.20
        
        score = 0.50
        
        if sentence_count >= 2:
            score += 0.20
        if sentence_count >= 3:
            score += 0.10
        
        if has_structure:
            score += 0.15
        
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        if 8 <= avg_words_per_sentence <= 30:
            score += 0.05
        
        return min(score, 1.0)
    
    @staticmethod
    def calculate_confidence_score(text: str) -> float:
        if AnswerMetrics.detect_manipulation_attempts(text):
            return 0.0
        
        if AnswerMetrics.detect_gibberish(text):
            return 0.0
        
        word_count = AnswerMetrics.calculate_word_count(text)
        completeness = AnswerMetrics.calculate_completeness_score(text)
        has_examples = AnswerMetrics.has_examples(text)
        has_metrics = AnswerMetrics.has_metrics_or_numbers(text)
        is_non_technical = AnswerMetrics.detect_non_technical_content(text)
        
        if word_count < 5:
            return 0.0
        elif word_count < 10:
            return 0.05
        elif word_count < 15:
            return 0.12
        
        if is_non_technical and word_count < 20:
            completeness = completeness * 0.3
        
        score = completeness * 0.5
        
        if word_count >= 40:
            score += 0.25
        elif word_count >= 25:
            score += 0.15
        elif word_count >= 15:
            score += 0.05
        
        if has_examples:
            score += 0.20
        
        if has_metrics:
            score += 0.15
        
        if is_non_technical:
            score = score * 0.4
        
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
