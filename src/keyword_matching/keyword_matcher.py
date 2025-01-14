from typing import List, Tuple, Dict
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from config.config import settings
from .keyword_repository import KeywordRepository
from difflib import SequenceMatcher
import numpy as np

class KeywordMatcher:
    def __init__(self, keyword_repository: KeywordRepository):
        # Download necessary NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        self.keyword_repository = keyword_repository
        self.min_similarity = 0.85  # Minimum similarity score for fuzzy matching
    
    def match(self, text: str) -> Tuple[List[str], float]:
        """Match text against keywords"""
        # Get keywords from repository
        keywords_dict = self.keyword_repository.get_all_keywords()
        
        # Tokenize and clean input text
        tokens = self._preprocess_text(text)
        
        # Find matches (including fuzzy matches)
        matches = self._find_matches(tokens, keywords_dict)
        
        if not matches:
            return [], 0.0
        
        # Sort by score and take top N
        sorted_matches = sorted(
            matches.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        top_keywords = [
            kw for kw, _ in sorted_matches[:settings.MAX_KEYWORDS]
        ]
        avg_score = float(np.mean([score for _, score in sorted_matches[:settings.MAX_KEYWORDS]]))
        
        return top_keywords, avg_score
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocess input text"""
        tokens = word_tokenize(text.lower())
        return [
            token for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]
    
    def _find_matches(self, tokens: List[str], keywords_dict: Dict[str, float]) -> Dict[str, float]:
        """Find matching keywords including fuzzy matches"""
        matches = {}
        
        for token in tokens:
            # Exact matches
            if token in keywords_dict:
                matches[token] = keywords_dict[token]
                continue
            
            # Fuzzy matches
            for keyword in keywords_dict:
                similarity = SequenceMatcher(None, token, keyword).ratio()
                if similarity >= self.min_similarity:
                    score = keywords_dict[keyword] * similarity
                    if keyword not in matches or score > matches[keyword]:
                        matches[keyword] = score
        
        return matches