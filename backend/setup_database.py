#!/usr/bin/env python3
"""
Interactive database setup script for AI Agents System.
This script helps configure database connection and create tables.
"""

import os
import sys
import getpass
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def get_database_config():
    """Get database configuration interactively."""
    print("=== AI Agents System - Database Setup ===\n")
    
    # Database type selection
    print("Select database type:")
    print("1. SQLite (local file)")
    print("2. PostgreSQL")
    print("3. MySQL")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    if choice == '1':
        # SQLite configuration
        db_file = input("Enter database file path (default: ./agent_ia.db): ").strip()
        if not db_file:
            db_file = "./agent_ia.db"
        database_url = f"sqlite:///{db_file}"
        
        return {
            'database_url': database_url,
            'database_type': 'sqlite',
            'echo': input("Enable SQL echo for debugging? (y/N): ").strip().lower() == 'y'
        }
    
    elif choice == '2':
        # PostgreSQL configuration
        host = input("Enter PostgreSQL host (default: localhost): ").strip() or "localhost"
        port = input("Enter PostgreSQL port (default: 5432): ").strip() or "5432"
        database = input("Enter database name (default: agent_ia): ").strip() or "agent_ia"
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ")
        
        database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        
        return {
            'database_url': database_url,
            'database_type': 'postgresql',
            'host': host,
            'port': port,
            'database': database,
            'username': username,
            'password': password,
            'echo': input("Enable SQL echo for debugging? (y/N): ").strip().lower() == 'y'
        }
    
    elif choice == '3':
        # MySQL configuration
        host = input("Enter MySQL host (default: localhost): ").strip() or "localhost"
        port = input("Enter MySQL port (default: 3306): ").strip() or "3306"
        database = input("Enter database name (default: agent_ia): ").strip() or "agent_ia"
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ")
        
        database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        
        return {
            'database_url': database_url,
            'database_type': 'mysql',
            'host': host,
            'port': port,
            'database': database,
            'username': username,
            'password': password,
            'echo': input("Enable SQL echo for debugging? (y/N): ").strip().lower() == 'y'
        }

def create_env_file(config):
    """Create or update .env file with database configuration."""
    env_file = Path(".env")
    
    # Read existing .env file if it exists
    env_content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Update or add database configuration
    lines = env_content.split('\n')
    updated_lines = []
    
    # Remove existing database configuration
    skip_next = False
    for line in lines:
        if line.startswith('DATABASE_URL=') or line.startswith('DATABASE_ECHO='):
            continue
        updated_lines.append(line)
    
    # Add new database configuration
    updated_lines.append(f"DATABASE_URL={config['database_url']}")
    updated_lines.append(f"DATABASE_ECHO={'true' if config['echo'] else 'false'}")
    
    # Write updated .env file
    with open(env_file, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"\nDatabase configuration saved to {env_file}")

def main():
    """Main function for database setup."""
    try:
        # Get database configuration
        config = get_database_config()
        
        # Create .env file
        create_env_file(config)
        
        print("\n=== Database Configuration Summary ===")
        print(f"Database Type: {config['database_type']}")
        print(f"Database URL: {config['database_url']}")
        print(f"SQL Echo: {'Enabled' if config['echo'] else 'Disabled'}")
        
        # Ask if user wants to create tables now
        create_tables_now = input("\nDo you want to create the database tables now? (Y/n): ").strip().lower()
        if create_tables_now != 'n':
            print("\nCreating database tables...")
            os.environ['DATABASE_URL'] = config['database_url']
            os.environ['DATABASE_ECHO'] = str(config['echo']).lower()
            
            # Import and run init_db
            from init_db import main as init_db_main
            init_db_main()
        
        print("\nDatabase setup completed successfully!")
        print("\nTo create tables later, run: python init_db.py")
        
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 