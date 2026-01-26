import re
from typing import List


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
    def detect_manipulation_attempts(text: str) -> bool:
        text_lower = text.lower()
        manipulation_patterns = [
            'help me', 'tell me', 'give me', 'dami', 'zi si mie', 'te rog', 'please give',
            'i need', 'i want', 'i beg', 'hai te rog', 'dami jobu', 'dami pace',
            'answer this', 'explain', 'do it for me', 'tell me the answer',
            'murit', 'bunicu', 'nevoie de bani', 'ingrop', 'died', 'grandpa',
            'nu stiu', "don't know", "i don't know", 'idk', 'no idea'
        ]
        return any(pattern in text_lower for pattern in manipulation_patterns)
    
    @staticmethod
    def detect_gibberish(text: str) -> bool:
        if len(text) < 10:
            return False
        
        words = text.split()
        text_lower = text.lower()
        total_chars = len(text.replace(' ', ''))
        
        gibberish_indicators = 0
        
        long_random_sequence = re.search(r'[a-z]{30,}', text_lower)
        if long_random_sequence:
            seq = long_random_sequence.group()
            unique_chars = len(set(seq))
            char_diversity = unique_chars / len(seq)
            if char_diversity < 0.5:
                gibberish_indicators += 3
        
        if len(words) >= 1:
            avg_word_length = sum(len(w) for w in words) / len(words)
            if avg_word_length > 15 and len(words) < 5:
                gibberish_indicators += 2
            
            very_long_words = sum(1 for w in words if len(w) > 20)
            if very_long_words >= 2:
                gibberish_indicators += 2
        
        random_char_sequences = re.findall(r'[a-z]{20,}', text_lower)
        if len(random_char_sequences) > 0:
            for seq in random_char_sequences:
                unique_chars = len(set(seq))
                if unique_chars < len(seq) * 0.4:
                    gibberish_indicators += 1
        
        repeated_chars = re.findall(r'(.)\1{5,}', text_lower)
        if len(repeated_chars) > 0:
            gibberish_indicators += 1
        
        if total_chars > 0:
            non_alpha_ratio = len(re.findall(r'[^a-zA-Z\s]', text)) / total_chars
            if non_alpha_ratio > 0.2 and len(words) < 6:
                gibberish_indicators += 1
        
        if len(words) == 1 and len(words[0]) > 30:
            gibberish_indicators += 2
        
        return gibberish_indicators >= 1
    
    @staticmethod
    def detect_non_technical_content(text: str) -> bool:
        text_lower = text.lower()
        technical_indicators = [
            'data', 'structure', 'algorithm', 'code', 'function', 'method', 'class',
            'system', 'design', 'implementation', 'performance', 'optimization',
            'database', 'api', 'framework', 'library', 'tool', 'technology',
            'project', 'application', 'software', 'development', 'programming'
        ]
        
        has_technical = any(indicator in text_lower for indicator in technical_indicators)
        
        if not has_technical and len(text.split()) > 5:
            return True
        
        return False
    
    @staticmethod
    def calculate_completeness_score(text: str) -> float:
        word_count = AnswerMetrics.calculate_word_count(text)
        
        if word_count >= 50:
            return 1.0
        elif word_count >= 30:
            return 0.8
        elif word_count >= 20:
            return 0.6
        elif word_count >= 15:
            return 0.4
        elif word_count >= 10:
            return 0.25
        else:
            return 0.05
