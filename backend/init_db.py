#!/usr/bin/env python3
"""
Database initialization script for AI Agents System.
This script creates all necessary tables and can be configured via environment variables.
"""

import os
import sys
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.conversation import Conversation
from app.models.chat_message import ChatMessage
from app.models.user import User
from app.models.token import Token

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_database_engine(database_url: str = None, echo: bool = False):
    """Create database engine with specified configuration."""
    if not database_url:
        database_url = settings.database_url
    
    logger.info(f"Connecting to database: {database_url}")
    
    # Configure engine based on database type
    if "sqlite" in database_url:
        connect_args = {"check_same_thread": False}
    else:
        connect_args = {}
    
    engine = create_engine(
        database_url,
        echo=echo,
        connect_args=connect_args
    )
    
    return engine

def test_database_connection(engine):
    """Test database connection."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def create_tables(engine):
    """Create all tables in the database."""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

def create_initial_data(engine):
    """Create initial data if needed."""
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if demo user exists
        demo_user = db.query(User).filter_by(username="demo_user").first()
        if not demo_user:
            logger.info("Creating demo user...")
            demo_user = User(
                username="demo_user",
                full_name="Demo User",
                email="demo@example.com",
                is_active=True,
                hashed_password="demo123"  # In production, this should be hashed
            )
            db.add(demo_user)
            db.commit()
            logger.info("Demo user created successfully")
        else:
            logger.info("Demo user already exists")
        
        db.close()
        return True
    except Exception as e:
        logger.error(f"Error creating initial data: {e}")
        return False

def main():
    """Main function to initialize the database."""
    logger.info("Starting database initialization...")
    
    # Get database configuration from environment or use defaults
    database_url = os.getenv('DATABASE_URL', settings.database_url)
    database_echo = os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
    
    logger.info(f"Database URL: {database_url}")
    logger.info(f"Database echo: {database_echo}")
    
    # Create engine
    engine = create_database_engine(database_url, database_echo)
    
    # Test connection
    if not test_database_connection(engine):
        logger.error("Cannot proceed without database connection")
        sys.exit(1)
    
    # Create tables
    if not create_tables(engine):
        logger.error("Failed to create tables")
        sys.exit(1)
    
    # Create initial data
    if not create_initial_data(engine):
        logger.error("Failed to create initial data")
        sys.exit(1)
    
    logger.info("Database initialization completed successfully!")

if __name__ == "__main__":
    main() 