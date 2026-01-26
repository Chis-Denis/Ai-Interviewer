from typing import List
from Application.Service.llm_data import AnswerData
from Application.Analysis.AnswerMetrics import AnswerMetrics
from Application.Analysis.AnswerEvaluator import AnswerEvaluator


class ScoringCalculator:
    
    @staticmethod
    def calculate_consistency_score(answers: List[AnswerData]) -> float:
        if len(answers) < 2:
            return 0.0
        
        word_counts = [AnswerMetrics.calculate_word_count(a.text) for a in answers]
        avg_length = sum(word_counts) / len(word_counts)
        
        if avg_length == 0:
            return 0.0
        
        mean = avg_length
        raw_variance = sum((x - mean) ** 2 for x in word_counts) / len(word_counts)
        standard_deviation = raw_variance ** 0.5
        coefficient_of_variation = standard_deviation / avg_length if avg_length > 0 else 1.0
        
        if coefficient_of_variation < 0.2:
            return 1.0
        elif coefficient_of_variation < 0.4:
            return 0.8
        elif coefficient_of_variation < 0.6:
            return 0.6
        elif coefficient_of_variation < 0.8:
            return 0.4
        else:
            return 0.2
    
    @staticmethod
    def calculate_overall_usefulness(
        clarity_score: float,
        confidence_score: float,
        consistency_score: float,
    ) -> float:
        base_score = (clarity_score + confidence_score + consistency_score) / 3.0
        
        return round(min(base_score, 1.0), 2)
    
    @staticmethod
    def calculate_all_scores(answers: List[AnswerData]) -> dict:
        if not answers:
            return {
                'consistency_score': 0.0,
                'overall_usefulness': 0.0,
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
            'consistency_score': round(consistency_score, 2),
            'overall_usefulness': overall_usefulness,
        }
