import re
from typing import List
from application.analysis.scoring_constants import ScoringConstants


class AnswerMetrics:
    
    @staticmethod
    def calculate_word_count(text: str) -> int:
        normalized_text = ' '.join(text.split())
        return len(normalized_text.split(ScoringConstants.TextProcessing.SPACE_CHAR)) if normalized_text else 0
    
    @staticmethod
    def calculate_sentence_count(text: str) -> int:
        text_processed = text
        for ending in ScoringConstants.TextProcessing.SENTENCE_ENDINGS[1:]:
            text_processed = text_processed.replace(ending, ScoringConstants.TextProcessing.PERIOD_REPLACEMENT)
        sentences = text_processed.split(ScoringConstants.TextProcessing.PERIOD_REPLACEMENT)
        return len([sentence for sentence in sentences if sentence.strip()])
    
    @staticmethod
    def _contains_keywords(text: str, keywords: List[str]) -> bool:
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    @staticmethod
    def has_structure_indicators(text: str) -> bool:
        return AnswerMetrics._contains_keywords(text, ScoringConstants.KeywordLists.STRUCTURE_KEYWORDS)
    
    @staticmethod
    def has_examples(text: str) -> bool:
        return AnswerMetrics._contains_keywords(text, ScoringConstants.KeywordLists.EXAMPLE_KEYWORDS)
    
    @staticmethod
    def has_metrics_or_numbers(text: str) -> bool:
        numbers = re.findall(ScoringConstants.RegexPatterns.NUMBERS_PATTERN, text)
        return len(numbers) > 0 or AnswerMetrics._contains_keywords(text, ScoringConstants.KeywordLists.METRIC_KEYWORDS)
    
    @staticmethod
    def detect_manipulation_attempts(text: str) -> bool:
        text_lower = text.lower()
        manipulation_patterns = ScoringConstants.KeywordLists.MANIPULATION_PATTERNS
        
        for pattern in manipulation_patterns:
            if pattern in text_lower:
                return True
        
        return False
    
    @staticmethod
    def detect_gibberish(text: str) -> bool:
        gib = ScoringConstants.GibberishDetection
        
        if len(text) < gib.MIN_TEXT_LENGTH:
            return False
        
        words = text.split(ScoringConstants.TextProcessing.SPACE_CHAR)
        text_lower = text.lower()
        total_chars = len(text.replace(ScoringConstants.TextProcessing.SPACE_CHAR, ''))
        
        gibberish_indicators = 0
        
        pattern_long = f'[a-z]{{{gib.LONG_RANDOM_SEQUENCE_LENGTH},}}'
        long_random_sequence = re.search(pattern_long, text_lower)
        if long_random_sequence:
            seq = long_random_sequence.group()
            unique_chars = len(set(seq))
            char_diversity = unique_chars / len(seq)
            if char_diversity < gib.CHAR_DIVERSITY_THRESHOLD:
                gibberish_indicators += gib.LONG_RANDOM_SEQUENCE_INDICATORS
        
        if len(words) >= 1:
            avg_word_length = sum(len(word) for word in words) / len(words)
            if avg_word_length > gib.AVG_WORD_LENGTH_THRESHOLD and len(words) < gib.MAX_WORDS_FOR_AVG_CHECK:
                gibberish_indicators += gib.AVG_WORD_LENGTH_INDICATORS
            
            very_long_words = sum(1 for word in words if len(word) > gib.VERY_LONG_WORD_LENGTH)
            if very_long_words >= gib.VERY_LONG_WORD_COUNT:
                gibberish_indicators += gib.VERY_LONG_WORD_INDICATORS
        
        pattern_random = f'[a-z]{{{gib.RANDOM_SEQUENCE_LENGTH},}}'
        random_char_sequences = re.findall(pattern_random, text_lower)
        if len(random_char_sequences) > 0:
            for seq in random_char_sequences:
                unique_chars = len(set(seq))
                if unique_chars < len(seq) * gib.RANDOM_SEQUENCE_DIVERSITY_THRESHOLD:
                    gibberish_indicators += 1
        
        pattern_repeated = f'(.)\\1{{{gib.REPEATED_CHAR_MIN_LENGTH},}}'
        repeated_chars = re.findall(pattern_repeated, text_lower)
        if len(repeated_chars) > 0:
            gibberish_indicators += 1
        
        if total_chars > 0:
            non_alpha_ratio = len(re.findall(ScoringConstants.RegexPatterns.NON_ALPHA_PATTERN, text)) / total_chars
            if non_alpha_ratio > gib.NON_ALPHA_RATIO_THRESHOLD and len(words) < gib.MAX_WORDS_FOR_NON_ALPHA_CHECK:
                gibberish_indicators += 1
        
        if len(words) == 1 and len(words[0]) > gib.SINGLE_WORD_LENGTH_THRESHOLD:
            gibberish_indicators += gib.SINGLE_WORD_INDICATORS
        
        return gibberish_indicators >= gib.MIN_INDICATORS_FOR_GIBBERISH
    
    @staticmethod
    def detect_non_technical_content(text: str) -> bool:
        text_lower = text.lower()
        has_technical = any(
            indicator in text_lower 
            for indicator in ScoringConstants.NonTechnicalDetection.TECHNICAL_INDICATORS
        )
        
        if not has_technical and len(text.split(ScoringConstants.TextProcessing.SPACE_CHAR)) > ScoringConstants.NonTechnicalDetection.MIN_WORDS_FOR_CHECK:
            return True
        
        return False
    
    @staticmethod
    def calculate_completeness_score(text: str) -> float:
        word_count = AnswerMetrics.calculate_word_count(text)
        thresholds = ScoringConstants.WordCountThresholds
        completeness = ScoringConstants.CompletenessScores
        
        if word_count >= thresholds.COMPREHENSIVE:
            return completeness.COMPREHENSIVE
        elif word_count >= thresholds.EXCELLENT:
            return completeness.EXCELLENT
        elif word_count >= thresholds.GOOD:
            return completeness.VERY_GOOD
        elif word_count >= thresholds.MEDIUM:
            return completeness.GOOD
        elif word_count >= thresholds.SHORT:
            return completeness.MEDIUM
        else:
            return completeness.LOW
