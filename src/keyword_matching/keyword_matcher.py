from typing import List, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from config.config import settings
import numpy as np

class KeywordMatcher:
    def __init__(self):
        # 下载必要的NLTK数据
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        
        # 加载停用词
        self.stop_words = set(stopwords.words('english'))
        
        # 这里可以加载预先准备好的高搜索率关键词库
        self.popular_keywords = self._load_popular_keywords()
    
    def _load_popular_keywords(self) -> dict:
        # 这里应该从数据库或文件中加载关键词
        # 临时返回示例数据
        return {
            "modern": 0.8,
            "vintage": 0.7,
            "luxury": 0.9,
            "casual": 0.6,
            # ... 更多关键词
        }
    
    def match(self, text: str) -> Tuple[List[str], float]:
        # 分词
        tokens = word_tokenize(text.lower())
        
        # 移除停用词
        tokens = [t for t in tokens if t not in self.stop_words]
        
        # 找到匹配的关键词
        matched_keywords = []
        scores = []
        
        for token in tokens:
            if token in self.popular_keywords:
                matched_keywords.append(token)
                scores.append(self.popular_keywords[token])
        
        # 选择得分最高的关键词
        if scores:
            avg_score = np.mean(scores)
            top_keywords = sorted(
                matched_keywords, 
                key=lambda k: self.popular_keywords[k],
                reverse=True
            )[:settings.MAX_KEYWORDS]
            
            return top_keywords, float(avg_score)
        
        return [], 0.0 