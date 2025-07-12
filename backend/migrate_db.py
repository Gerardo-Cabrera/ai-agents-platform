#!/usr/bin/env python3
"""
Database migration script for AI Agents System.
This script handles database schema updates and migrations.
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text, inspect
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

def get_current_schema_version(engine):
    """Get current schema version from database."""
    try:
        with engine.connect() as connection:
            # Check if schema_version table exists
            inspector = inspect(engine)
            if 'schema_version' not in inspector.get_table_names():
                return 0
            
            result = connection.execute(text("SELECT version FROM schema_version ORDER BY id DESC LIMIT 1"))
            row = result.fetchone()
            return row[0] if row else 0
    except Exception as e:
        logger.warning(f"Could not get schema version: {e}")
        return 0

def update_schema_version(engine, version):
    """Update schema version in database."""
    try:
        with engine.connect() as connection:
            # Create schema_version table if it doesn't exist
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    id SERIAL PRIMARY KEY,
                    version INTEGER NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Insert new version
            connection.execute(text("INSERT INTO schema_version (version) VALUES (:version)"), {"version": version})
            connection.commit()
            logger.info(f"Schema version updated to {version}")
    except Exception as e:
        logger.error(f"Error updating schema version: {e}")

def run_migration_1(engine):
    """Migration 1: Create initial tables."""
    logger.info("Running migration 1: Create initial tables")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Migration 1 completed successfully")
        return True
    except Exception as e:
        logger.error(f"Migration 1 failed: {e}")
        return False

def run_migration_2(engine):
    """Migration 2: Add indexes for performance."""
    logger.info("Running migration 2: Add performance indexes")
    
    try:
        with engine.connect() as connection:
            # Add indexes for better performance
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_conversations_user_id 
                ON conversations(user_id)
            """))
            
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation_id 
                ON chat_messages(conversation_id)
            """))
            
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp 
                ON chat_messages(timestamp)
            """))
            
            connection.commit()
            logger.info("Migration 2 completed successfully")
            return True
    except Exception as e:
        logger.error(f"Migration 2 failed: {e}")
        return False

def run_migrations(engine, target_version=None):
    """Run all pending migrations."""
    current_version = get_current_schema_version(engine)
    logger.info(f"Current schema version: {current_version}")
    
    if target_version is None:
        target_version = 2  # Latest version
    
    if current_version >= target_version:
        logger.info("Database is already up to date")
        return True
    
    # Define migrations
    migrations = {
        1: run_migration_1,
        2: run_migration_2,
    }
    
    # Run pending migrations
    for version in range(current_version + 1, target_version + 1):
        if version in migrations:
            logger.info(f"Running migration {version}...")
            if not migrations[version](engine):
                logger.error(f"Migration {version} failed")
                return False
            
            # Update schema version
            update_schema_version(engine, version)
        else:
            logger.warning(f"No migration defined for version {version}")
    
    logger.info("All migrations completed successfully")
    return True

def main():
    """Main function for database migration."""
    logger.info("Starting database migration...")
    
    # Get database configuration
    database_url = os.getenv('DATABASE_URL', settings.database_url)
    database_echo = os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
    
    logger.info(f"Database URL: {database_url}")
    
    # Create engine
    if "sqlite" in database_url:
        connect_args = {"check_same_thread": False}
    else:
        connect_args = {}
    
    engine = create_engine(
        database_url,
        echo=database_echo,
        connect_args=connect_args
    )
    
    # Test connection
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations(engine):
        logger.error("Migration failed")
        sys.exit(1)
    
    logger.info("Database migration completed successfully!")

if __name__ == "__main__":
    main() 