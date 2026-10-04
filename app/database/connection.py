"""
Database connection management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config import get_settings

settings = get_settings()

# Create engine based on database URL
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},  # SQLite specific
        echo=settings.debug,
    )
else:
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
