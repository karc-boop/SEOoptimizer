import os
import sys
import pytest

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.text_processing.text_preprocessor import TextPreprocessor

@pytest.fixture
def preprocessor():
    return TextPreprocessor()

def test_clean_text(preprocessor):
    text = "Hello, World! This is a TEST...   with   spaces"
    cleaned = preprocessor.clean_text(text)
    assert cleaned == "hello world this is a test with spaces"

def test_process(preprocessor):
    text = "The modern luxury furniture with vintage design elements"
    result = preprocessor.process(text)
    
    assert 'cleaned_text' in result
    assert 'tokens' in result
    assert 'key_phrases' in result
    assert 'sentences' in result
    
    # Check if key phrases were extracted
    assert len(result['key_phrases']) > 0
    assert 'modern luxury furniture' in result['key_phrases']
    
    # Check if tokens were processed
    assert 'modern' in result['tokens']
    assert 'luxury' in result['tokens']
    assert 'furniture' in result['tokens']

def test_extract_key_phrases(preprocessor):
    tagged_tokens = [
        ('modern', 'JJ'),
        ('luxury', 'NN'),
        ('furniture', 'NN'),
        ('with', 'IN'),
        ('vintage', 'JJ'),
        ('design', 'NN')
    ]
    
    phrases = preprocessor.extract_key_phrases(tagged_tokens)
    assert 'modern luxury furniture' in phrases
    assert 'vintage design' in phrases 