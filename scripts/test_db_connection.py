import os
import sys

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from database.database import get_db
from database.models import ProductName, Keyword

def test_connection():
    """Test database connection and tables"""
    try:
        with get_db() as db:
            # Test query
            keywords = db.query(Keyword).limit(5).all()
            print("Database connection successful!")
            print(f"Found {len(keywords)} keywords in database")
            return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    test_connection()