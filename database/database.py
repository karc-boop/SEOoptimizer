from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from config.config import settings
from contextlib import contextmanager

# Create database engine
engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """get database session context manager"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """initialize database tables"""
    from .models import Base
    Base.metadata.create_all(bind=engine) 