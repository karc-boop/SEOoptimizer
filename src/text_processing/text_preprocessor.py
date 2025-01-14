import re
from typing import List, Dict
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag import pos_tag

class TextPreprocessor:
    def __init__(self):
        # Download necessary NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('omw-1.4')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text: str) -> str:
        """Basic text cleaning"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces between words
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def get_wordnet_pos(self, tag: str) -> str:
        """Map POS tag to WordNet POS tag"""
        tag_dict = {
            'J': wordnet.ADJ,
            'N': wordnet.NOUN,
            'V': wordnet.VERB,
            'R': wordnet.ADV
        }
        return tag_dict.get(tag[0], wordnet.NOUN)
    
    def process(self, text: str) -> Dict[str, any]:
        """
        Process text and return detailed analysis
        Returns:
            Dict containing:
            - cleaned_text: basic cleaned text
            - tokens: list of processed tokens
            - key_phrases: extracted key phrases
            - sentences: list of sentences
        """
        # Basic cleaning
        cleaned_text = self.clean_text(text)
        
        # Tokenize into sentences
        sentences = sent_tokenize(cleaned_text)
        
        # Process tokens
        tokens = word_tokenize(cleaned_text)
        
        # POS tagging
        tagged_tokens = pos_tag(tokens)
        
        # Process tokens with POS info
        processed_tokens = []
        for token, tag in tagged_tokens:
            if (token not in self.stop_words and 
                len(token) > 2 and 
                token.isalnum()):
                # Lemmatize with POS tag
                lemma = self.lemmatizer.lemmatize(
                    token, 
                    self.get_wordnet_pos(tag)
                )
                processed_tokens.append(lemma)
        
        # Extract key phrases
        key_phrases = self.extract_key_phrases(tagged_tokens)
        
        return {
            'cleaned_text': cleaned_text,
            'tokens': processed_tokens,
            'key_phrases': key_phrases,
            'sentences': sentences
        }
    
    def extract_key_phrases(self, tagged_tokens: List[tuple]) -> List[str]:
        """Extract meaningful phrases from tagged tokens"""
        key_phrases = []
        current_phrase = []
        
        for token, tag in tagged_tokens:
            # Consider nouns, adjectives, and verbs
            if tag.startswith(('NN', 'JJ', 'VB')):
                current_phrase.append(token)
                # Add sub-phrases of length 2 or more
                if len(current_phrase) >= 2:
                    key_phrases.append(' '.join(current_phrase[-2:]))
            else:
                if len(current_phrase) > 0:
                    phrase = ' '.join(current_phrase)
                    if len(phrase.split()) > 1:
                        key_phrases.append(phrase)
                    current_phrase = []
        
        # Add the last phrase if exists
        if current_phrase:
            phrase = ' '.join(current_phrase)
            if len(phrase.split()) > 1:
                key_phrases.append(phrase)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(key_phrases))