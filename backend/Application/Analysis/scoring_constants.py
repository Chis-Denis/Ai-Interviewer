class ScoringConstants:
    
    MIN_ANSWERS_FOR_CONSISTENCY = 2
    SCORE_PRECISION = 2
    MAX_SCORE = 1.0
    MIN_SCORE = 0.0
    
    ZERO_SCORE = 0.0
    BAD_ANSWER_THRESHOLD_RATIO = 0.5
    LOW_CONSISTENCY_PENALTY = 0.1
    
    class WordCountThresholds:
        VERY_SHORT = 5
        SHORT = 10
        MEDIUM = 15
        GOOD = 20
        VERY_GOOD = 25
        EXCELLENT = 30
        OUTSTANDING = 40
        COMPREHENSIVE = 50
    
    class ClarityScores:
        VERY_SHORT_PENALTY = 0.02
        SHORT_PENALTY = 0.08
        MEDIUM_PENALTY = 0.20
        BASE_SCORE = 0.50
        
        TWO_SENTENCES_BONUS = 0.20
        THREE_SENTENCES_BONUS = 0.10
        STRUCTURE_BONUS = 0.15
        OPTIMAL_SENTENCE_LENGTH_BONUS = 0.05
        
        MIN_WORDS_PER_SENTENCE = 8
        MAX_WORDS_PER_SENTENCE = 30
    
    class ConfidenceScores:
        VERY_SHORT_PENALTY = 0.0
        SHORT_PENALTY = 0.05
        MEDIUM_PENALTY = 0.12
        
        COMPLETENESS_WEIGHT = 0.5
        NON_TECHNICAL_SHORT_PENALTY_MULTIPLIER = 0.3
        NON_TECHNICAL_PENALTY_MULTIPLIER = 0.4
        
        OUTSTANDING_LENGTH_BONUS = 0.25
        VERY_GOOD_LENGTH_BONUS = 0.15
        GOOD_LENGTH_BONUS = 0.05
        
        EXAMPLES_BONUS = 0.20
        METRICS_BONUS = 0.15
    
    class CompletenessScores:
        COMPREHENSIVE = 1.0
        EXCELLENT = 0.8
        VERY_GOOD = 0.6
        GOOD = 0.4
        MEDIUM = 0.25
        LOW = 0.05
    
    class ConsistencyScores:
        VERY_SHORT_AVG_PENALTY = 0.05
        SHORT_AVG_PENALTY = 0.15
        
        PERFECT_CONSISTENCY = 1.0
        HIGH_CONSISTENCY = 0.8
        MEDIUM_CONSISTENCY = 0.6
        LOW_CONSISTENCY = 0.4
        POOR_CONSISTENCY = 0.2
        
        COEFFICIENT_VARIATION_EXCELLENT = 0.2
        COEFFICIENT_VARIATION_GOOD = 0.4
        COEFFICIENT_VARIATION_MEDIUM = 0.6
        COEFFICIENT_VARIATION_LOW = 0.8
    
    class OverallUsefulness:
        SCORE_DIVISOR = 3.0
    
    class GibberishDetection:
        MIN_TEXT_LENGTH = 10
        LONG_RANDOM_SEQUENCE_LENGTH = 30
        CHAR_DIVERSITY_THRESHOLD = 0.5
        LONG_RANDOM_SEQUENCE_INDICATORS = 3
        
        AVG_WORD_LENGTH_THRESHOLD = 15
        MAX_WORDS_FOR_AVG_CHECK = 5
        AVG_WORD_LENGTH_INDICATORS = 2
        
        VERY_LONG_WORD_LENGTH = 20
        VERY_LONG_WORD_COUNT = 2
        VERY_LONG_WORD_INDICATORS = 2
        
        RANDOM_SEQUENCE_LENGTH = 20
        RANDOM_SEQUENCE_DIVERSITY_THRESHOLD = 0.4
        
        REPEATED_CHAR_MIN_LENGTH = 5
        
        NON_ALPHA_RATIO_THRESHOLD = 0.2
        MAX_WORDS_FOR_NON_ALPHA_CHECK = 6
        
        SINGLE_WORD_LENGTH_THRESHOLD = 30
        SINGLE_WORD_INDICATORS = 2
        
        MIN_INDICATORS_FOR_GIBBERISH = 1
    
    class NonTechnicalDetection:
        MIN_WORDS_FOR_CHECK = 5
        TECHNICAL_INDICATORS = [
            'data', 'structure', 'algorithm', 'code', 'function', 'method', 'class',
            'system', 'design', 'implementation', 'performance', 'optimization',
            'database', 'api', 'framework', 'library', 'tool', 'technology',
            'project', 'application', 'software', 'development', 'programming'
        ]
    
    class KeywordLists:
        STRUCTURE_KEYWORDS = [
            'because', 'since', 'when', 'if', 'then', 'therefore', 'however', 'although',
            'first', 'second', 'finally', 'in addition', 'furthermore', 'moreover'
        ]
        
        EXAMPLE_KEYWORDS = [
            'example', 'instance', 'case', 'such as', 'for instance', 'like', 'e.g.', 'including'
        ]
        
        METRIC_KEYWORDS = [
            'percent', '%', 'times', 'x', 'increase', 'decrease', 'rate', 'ratio'
        ]
        
        MANIPULATION_PATTERNS = [
            'help me', 'tell me', 'give me', 'dami', 'zi si mie', 'te rog', 'please give',
            'i need', 'i want', 'i beg', 'hai te rog', 'dami jobu', 'dami pace',
            'answer this', 'explain', 'do it for me', 'tell me the answer',
            'murit', 'bunicu', 'nevoie de bani', 'ingrop', 'died', 'grandpa',
            'nu stiu', "don't know", "i don't know", 'idk', 'no idea'
        ]
    
    class RegexPatterns:
        NUMBERS_PATTERN = r'\d+'
        NON_ALPHA_PATTERN = r'[^a-zA-Z\s]'
    
    class TextProcessing:
        SENTENCE_ENDINGS = ['.', '!', '?']
        PERIOD_REPLACEMENT = '.'
        SPACE_CHAR = ' '
    
    class Rounding:
        SCORE_DECIMAL_PLACES = 2
