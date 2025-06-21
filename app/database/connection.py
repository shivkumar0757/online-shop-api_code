"""
Database connection and session management
"""
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends


# Database URL - SQLite for simplicity
DATABASE_URL = "sqlite:///./shop.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session


# Dependency for database session
SessionDep = Annotated[Session, Depends(get_session)]
