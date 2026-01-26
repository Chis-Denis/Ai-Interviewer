from typing import List
from Application.Services.llm_data import AnswerData
from Application.Analysis.AnswerMetrics import AnswerMetrics
from Application.Analysis.AnswerEvaluator import AnswerEvaluator
from Application.Analysis.scoring_constants import ScoringConstants


class ScoringCalculator:
    
    @staticmethod
    def calculate_consistency_score(answers: List[AnswerData]) -> float:
        if len(answers) < ScoringConstants.MIN_ANSWERS_FOR_CONSISTENCY:
            return ScoringConstants.ZERO_SCORE
        
        manipulation_count = sum(1 for a in answers if AnswerMetrics.detect_manipulation_attempts(a.text))
        gibberish_count = sum(1 for a in answers if AnswerMetrics.detect_gibberish(a.text))
        
        if manipulation_count > 0 or gibberish_count > 0:
            bad_answer_ratio = (manipulation_count + gibberish_count) / len(answers)
            if bad_answer_ratio >= ScoringConstants.BAD_ANSWER_THRESHOLD_RATIO:
                return ScoringConstants.ZERO_SCORE
            else:
                return ScoringConstants.LOW_CONSISTENCY_PENALTY
        
        word_counts = [AnswerMetrics.calculate_word_count(a.text) for a in answers]
        avg_length = sum(word_counts) / len(word_counts)
        thresholds = ScoringConstants.WordCountThresholds
        consistency = ScoringConstants.ConsistencyScores
        
        if avg_length == ScoringConstants.ZERO_SCORE:
            return ScoringConstants.ZERO_SCORE
        
        if avg_length < thresholds.VERY_SHORT:
            return consistency.VERY_SHORT_AVG_PENALTY
        elif avg_length < thresholds.SHORT:
            return consistency.SHORT_AVG_PENALTY
        
        mean = avg_length
        raw_variance = sum((x - mean) ** 2 for x in word_counts) / len(word_counts)
        standard_deviation = raw_variance ** 0.5
        coefficient_of_variation = standard_deviation / avg_length if avg_length > 0 else ScoringConstants.MAX_SCORE
        
        if coefficient_of_variation < consistency.COEFFICIENT_VARIATION_EXCELLENT:
            return consistency.PERFECT_CONSISTENCY
        elif coefficient_of_variation < consistency.COEFFICIENT_VARIATION_GOOD:
            return consistency.HIGH_CONSISTENCY
        elif coefficient_of_variation < consistency.COEFFICIENT_VARIATION_MEDIUM:
            return consistency.MEDIUM_CONSISTENCY
        elif coefficient_of_variation < consistency.COEFFICIENT_VARIATION_LOW:
            return consistency.LOW_CONSISTENCY
        else:
            return consistency.POOR_CONSISTENCY
    
    @staticmethod
    def calculate_overall_usefulness(
        clarity_score: float,
        confidence_score: float,
        consistency_score: float,
    ) -> float:
        base_score = (clarity_score + confidence_score + consistency_score) / ScoringConstants.OverallUsefulness.SCORE_DIVISOR
        
        return round(min(base_score, ScoringConstants.MAX_SCORE), ScoringConstants.SCORE_PRECISION)
    
    @staticmethod
    def calculate_all_scores(answers: List[AnswerData]) -> dict:
        if not answers:
            return {
                'consistency_score': ScoringConstants.ZERO_SCORE,
                'overall_usefulness': ScoringConstants.ZERO_SCORE,
            }
        
        evaluation_result = AnswerEvaluator.evaluate_all_answers(answers)
        
        clarity_score = evaluation_result['clarity_score']
        confidence_score = evaluation_result['confidence_score']
        
        consistency_score = ScoringCalculator.calculate_consistency_score(answers)
        
        overall_usefulness = ScoringCalculator.calculate_overall_usefulness(
            clarity_score=clarity_score,
            confidence_score=confidence_score,
            consistency_score=consistency_score,
        )
        
        return {
            'consistency_score': round(consistency_score, ScoringConstants.SCORE_PRECISION),
            'overall_usefulness': overall_usefulness,
        }
