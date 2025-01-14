import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.product_naming.name_generator import NameGenerator

@pytest.fixture
def mock_vertex_client():
    with patch('src.product_naming.vertex_ai_client.VertexAIClient') as mock:
        client = mock.return_value
        client.generate_text.return_value = "TestProduct Pro"
        yield client

@pytest.fixture
def generator(mock_vertex_client):
    return NameGenerator()

def test_generate_name(generator):
    keywords = ["modern", "luxury", "comfort"]
    name = generator.generate(keywords)
    
    assert name is not None
    assert isinstance(name, str)
    assert len(name) > 0

def test_build_prompt(generator):
    keywords = ["modern", "luxury"]
    prompt = generator._build_prompt(keywords)
    
    assert "modern, luxury" in prompt
    assert "Requirements:" in prompt
    assert "Product name:" in prompt

def test_process_response(generator):
    # Test with quotes
    assert generator._process_response('"Test Product"') == "Test Product"
    
    # Test with multiple lines
    assert generator._process_response('Test\nProduct') == "Test"
    
    # Test capitalization
    assert generator._process_response('test product') == "Test Product"

def test_generate_name_failure(generator, mock_vertex_client):
    mock_vertex_client.generate_text.return_value = None
    
    keywords = ["modern", "luxury"]
    name = generator.generate(keywords)
    
    assert name is None 