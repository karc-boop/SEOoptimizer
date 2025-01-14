from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from database.models import Keyword
from functools import lru_cache
import time

'''
KeywordRepository is a class that interacts with the database to get keywords and their scores.
'''
class KeywordRepository:
    def __init__(self, db: Session):
        self.db = db
        self._cache_timestamp = 0
        self._cache_ttl = 3600  # 1 hour cache TTL
        
    @lru_cache(maxsize=1)
    def get_all_keywords(self) -> Dict[str, float]:
        """
        Get all keywords with their scores
        Returns a dict of keyword -> relevance_score
        """
        current_time = time.time()
        
        # Check if cache needs refresh
        if current_time - self._cache_timestamp > self._cache_ttl:
            self._cache_timestamp = current_time
            # Clear the LRU cache
            self.get_all_keywords.cache_clear()
        
        keywords = self.db.query(Keyword).all()
        return {
            kw.keyword: self._calculate_score(kw)
            for kw in keywords
        }
    
    def _calculate_score(self, keyword: Keyword) -> float:
        """Calculate final score based on multiple factors"""
        # Normalize search volume (0-1)
        volume_score = min(keyword.search_volume / 1000, 1.0)
        
        # Combine scores with weights
        weights = {
            'relevance': 0.4,
            'competition': 0.3,
            'volume': 0.3
        }
        
        final_score = (
            keyword.relevance_score * weights['relevance'] +
            (1 - keyword.competition_score) * weights['competition'] +
            volume_score * weights['volume']
        )
        
        return round(final_score, 3)
    
    def add_keyword(self, keyword_data: Dict) -> Keyword:
        """Add new keyword to database"""
        keyword = Keyword(**keyword_data)
        self.db.add(keyword)
        self.db.commit()
        self.db.refresh(keyword)
        # Clear cache
        self.get_all_keywords.cache_clear()
        return keyword
    
    def update_scores(self, keyword_id: int, scores: Dict[str, float]) -> Optional[Keyword]:
        """Update keyword scores"""
        keyword = self.db.query(Keyword).filter(Keyword.id == keyword_id).first()
        if keyword:
            for field, value in scores.items():
                setattr(keyword, field, value)
            self.db.commit()
            # Clear cache
            self.get_all_keywords.cache_clear()
        return keyword 