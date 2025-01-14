import os
import sys
import pytest
from sqlalchemy import text

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.keyword_matching.keyword_matcher import KeywordMatcher
from src.keyword_matching.keyword_repository import KeywordRepository
from database.database import get_db
from database.models import Keyword, Base

@pytest.fixture(autouse=True)
def setup_database():
    """Reset database before each test to ensure a clean state"""
    with get_db() as db:
        # Drop all tables
        Base.metadata.drop_all(bind=db.get_bind())
        # Create all tables
        Base.metadata.create_all(bind=db.get_bind())

@pytest.fixture
def db():
    with get_db() as session:
        yield session

@pytest.fixture
def repository(db):
    return KeywordRepository(db)

@pytest.fixture
def matcher(repository):
    return KeywordMatcher(repository)

def test_exact_match(matcher, db):
    # Add test keywords
    keyword = Keyword(
        keyword="modern",
        search_volume=1000,
        competition_score=0.5,
        relevance_score=0.9
    )
    db.add(keyword)
    db.commit()
    
    text = "I want a modern design"
    keywords, score = matcher.match(text)
    
    assert "modern" in keywords
    assert score > 0.0

def test_fuzzy_match(matcher, db):
    keyword = Keyword(
        keyword="vintage",
        search_volume=800,
        competition_score=0.4,
        relevance_score=0.8
    )
    db.add(keyword)
    db.commit()
    
    text = "I want a vintag style"  # Misspelled
    keywords, score = matcher.match(text)
    
    assert "vintage" in keywords
    assert score > 0.0

def test_no_match(matcher):
    text = "xyz123"
    keywords, score = matcher.match(text)
    
    assert len(keywords) == 0
    assert score == 0.0 