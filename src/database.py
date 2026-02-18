"""
Database configuration and session management
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use SQLite as fallback for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./mergington_school.db"  # SQLite fallback for local development
)

# Create database engine
# For PostgreSQL in production, DATABASE_URL should be like:
# postgresql://username:password@localhost:5432/dbname
engine = create_engine(
    DATABASE_URL,
    # SQLite specific - remove for PostgreSQL
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=True  # Set to False in production
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    """
    Base.metadata.create_all(bind=engine)
