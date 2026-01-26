from typing import List
from Application.Services.llm_data import AnswerData
from Application.Analysis.AnswerMetrics import AnswerMetrics
from Application.Analysis.scoring_constants import ScoringConstants


class AnswerEvaluator:
    
    @staticmethod
    def calculate_clarity_score(text: str) -> float:
        if AnswerMetrics.detect_manipulation_attempts(text):
            return ScoringConstants.ZERO_SCORE
        
        if AnswerMetrics.detect_gibberish(text):
            return ScoringConstants.ZERO_SCORE
        
        word_count = AnswerMetrics.calculate_word_count(text)
        sentence_count = AnswerMetrics.calculate_sentence_count(text)
        has_structure = AnswerMetrics.has_structure_indicators(text)
        thresholds = ScoringConstants.WordCountThresholds
        clarity = ScoringConstants.ClarityScores
        
        if word_count < thresholds.VERY_SHORT:
            return clarity.VERY_SHORT_PENALTY
        elif word_count < thresholds.SHORT:
            return clarity.SHORT_PENALTY
        elif word_count < thresholds.MEDIUM:
            return clarity.MEDIUM_PENALTY
        
        score = clarity.BASE_SCORE
        
        if sentence_count >= 2:
            score += clarity.TWO_SENTENCES_BONUS
        if sentence_count >= 3:
            score += clarity.THREE_SENTENCES_BONUS
        
        if has_structure:
            score += clarity.STRUCTURE_BONUS
        
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        if clarity.MIN_WORDS_PER_SENTENCE <= avg_words_per_sentence <= clarity.MAX_WORDS_PER_SENTENCE:
            score += clarity.OPTIMAL_SENTENCE_LENGTH_BONUS
        
        return min(score, ScoringConstants.MAX_SCORE)
    
    @staticmethod
    def calculate_confidence_score(text: str) -> float:
        if AnswerMetrics.detect_manipulation_attempts(text):
            return ScoringConstants.ZERO_SCORE
        
        if AnswerMetrics.detect_gibberish(text):
            return ScoringConstants.ZERO_SCORE
        
        word_count = AnswerMetrics.calculate_word_count(text)
        completeness = AnswerMetrics.calculate_completeness_score(text)
        has_examples = AnswerMetrics.has_examples(text)
        has_metrics = AnswerMetrics.has_metrics_or_numbers(text)
        is_non_technical = AnswerMetrics.detect_non_technical_content(text)
        thresholds = ScoringConstants.WordCountThresholds
        confidence = ScoringConstants.ConfidenceScores
        
        if word_count < thresholds.VERY_SHORT:
            return confidence.VERY_SHORT_PENALTY
        elif word_count < thresholds.SHORT:
            return confidence.SHORT_PENALTY
        elif word_count < thresholds.MEDIUM:
            return confidence.MEDIUM_PENALTY
        
        if is_non_technical and word_count < thresholds.GOOD:
            completeness = completeness * confidence.NON_TECHNICAL_SHORT_PENALTY_MULTIPLIER
        
        score = completeness * confidence.COMPLETENESS_WEIGHT
        
        if word_count >= thresholds.OUTSTANDING:
            score += confidence.OUTSTANDING_LENGTH_BONUS
        elif word_count >= thresholds.VERY_GOOD:
            score += confidence.VERY_GOOD_LENGTH_BONUS
        elif word_count >= thresholds.MEDIUM:
            score += confidence.GOOD_LENGTH_BONUS
        
        if has_examples:
            score += confidence.EXAMPLES_BONUS
        
        if has_metrics:
            score += confidence.METRICS_BONUS
        
        if is_non_technical:
            score = score * confidence.NON_TECHNICAL_PENALTY_MULTIPLIER
        
        return min(score, ScoringConstants.MAX_SCORE)
    
    @staticmethod
    def evaluate_all_answers(answers: List[AnswerData]) -> dict:
        if not answers:
            return {
                'clarity_score': ScoringConstants.ZERO_SCORE,
                'confidence_score': ScoringConstants.ZERO_SCORE,
            }
        
        clarity_scores = [AnswerEvaluator.calculate_clarity_score(a.text) for a in answers]
        confidence_scores = [AnswerEvaluator.calculate_confidence_score(a.text) for a in answers]
        
        avg_clarity = sum(clarity_scores) / len(clarity_scores)
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        return {
            'clarity_score': round(avg_clarity, ScoringConstants.SCORE_PRECISION),
            'confidence_score': round(avg_confidence, ScoringConstants.SCORE_PRECISION),
        }
