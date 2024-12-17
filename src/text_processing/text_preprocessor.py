import re
from typing import List
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        # 下载必要的NLTK数据
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def process(self, text: str) -> str:
        """
        预处理文本
        1. 转换为小写
        2. 移除特殊字符
        3. 分词
        4. 移除停用词
        5. 词形还原
        """
        # 转换为小写
        text = text.lower()
        
        # 移除特殊字符
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 分词
        tokens = word_tokenize(text)
        
        # 移除停用词和词形还原
        processed_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]
        
        # 重新组合为文本
        return ' '.join(processed_tokens)
    
    def extract_key_phrases(self, text: str) -> List[str]:
        """提取关键短语"""
        # 分词和词性标注
        tokens = word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        
        # 提取名词短语
        phrases = []
        current_phrase = []
        
        for word, tag in tagged:
            if tag.startswith(('NN', 'JJ')):  # 名词和形容词
                current_phrase.append(word)
            else:
                if current_phrase:
                    phrases.append(' '.join(current_phrase))
                    current_phrase = []
        
        if current_phrase:
            phrases.append(' '.join(current_phrase))
        
        return phrases 