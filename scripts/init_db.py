"""Initialize the database."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from backend.models.doctor import Base
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize the database."""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///database/healthcare.db')
    
    # Create database directory if needed
    db_path = database_url.replace('sqlite:///', '')
    if not db_path.startswith('/'):
        db_path = os.path.join(os.getcwd(), db_path)
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Create tables
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    print(f"Database initialized at: {database_url}")

if __name__ == '__main__':
    init_database()
