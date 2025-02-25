"""
Database Configuration Module.

This module sets up the database connection, session management,
and base model for SQLAlchemy ORM.
"""

import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

# Load .env environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine and session
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/inventory_db")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Gets a new database session.
    Ensures proper session closure after use.
    """
    db = SessionLocal()
    logger.debug("New DB session opened.")
    try:
        yield db
    finally:
        db.close()
        logger.debug("DB session closed.")
