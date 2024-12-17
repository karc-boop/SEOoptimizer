import os
import sys

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from database.database import init_db, get_db
from database.models import Keyword
import csv
from typing import List, Dict

def load_initial_keywords(filepath: str) -> List[Dict]:
    """Load initial keywords from CSV file"""
    keywords = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keywords.append({
                'keyword': row['keyword'],
                'search_volume': int(row['search_volume']),
                'competition_score': float(row['competition_score']),
                'relevance_score': float(row['relevance_score'])
            })
    return keywords

def populate_keywords(keywords: List[Dict]):
    """Populate keywords table with initial data"""
    with get_db() as db:
        for kw_data in keywords:
            keyword = Keyword(**kw_data)
            db.add(keyword)
        db.commit()

def main():
    """Initialize database and load initial data"""
    print("Initializing database...")
    init_db()
    
    print("Loading initial keywords...")
    keywords = load_initial_keywords('data/initial_keywords.csv')
    
    print("Populating database...")
    populate_keywords(keywords)
    
    print("Database initialization completed!")

if __name__ == "__main__":
    main() 