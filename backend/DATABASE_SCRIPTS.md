# Database Scripts Documentation

This directory contains scripts for managing the AI Agents System database.

## Scripts Overview

### 1. `setup_database.py` - Interactive Database Setup
**Purpose**: Interactive script to configure database connection and create initial setup.

**Usage**:
```bash
python setup_database.py
```

**Features**:
- Supports SQLite, PostgreSQL, and MySQL
- Interactive configuration prompts
- Automatically creates/updates `.env` file
- Option to create tables immediately

**Example Output**:
```
=== AI Agents System - Database Setup ===

Select database type:
1. SQLite (local file)
2. PostgreSQL
3. MySQL

Enter your choice (1-3): 2
Enter PostgreSQL host (default: localhost): 
Enter PostgreSQL port (default: 5432): 
Enter database name (default: agent_ia): 
Enter username: myuser
Enter password: ********
Enable SQL echo for debugging? (y/N): n

Database configuration saved to .env

=== Database Configuration Summary ===
Database Type: postgresql
Database URL: postgresql://myuser:password@localhost:5432/agent_ia
SQL Echo: Disabled

Do you want to create the database tables now? (Y/n): y

Creating database tables...
Database setup completed successfully!
```

### 2. `init_db.py` - Database Initialization
**Purpose**: Creates all database tables and initial data.

**Usage**:
```bash
python init_db.py
```

**Features**:
- Creates all necessary tables
- Creates demo user if not exists
- Uses configuration from `.env` file
- Detailed logging

**Environment Variables**:
- `DATABASE_URL`: Database connection string
- `DATABASE_ECHO`: Enable SQL echo (true/false)

### 3. `migrate_db.py` - Database Migration
**Purpose**: Handles database schema updates and migrations.

**Usage**:
```bash
python migrate_db.py
```

**Features**:
- Version-based migrations
- Automatic schema version tracking
- Performance optimizations
- Safe migration execution

## Database Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database
DATABASE_ECHO=false
```

### Supported Database Types

#### 1. SQLite (Development)
```env
DATABASE_URL=sqlite:///./agent_ia.db
```

#### 2. PostgreSQL (Production)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/agent_ia
```

#### 3. MySQL (Production)
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/agent_ia
```

## Quick Start

### For New Installation:
1. **Setup database configuration**:
   ```bash
   python setup_database.py
   ```

2. **Create tables** (if not done in setup):
   ```bash
   python init_db.py
   ```

### For Existing Installation:
1. **Run migrations**:
   ```bash
   python migrate_db.py
   ```

## Docker Usage

### Inside Docker Container:
```bash
# Setup database
docker compose exec backend python setup_database.py

# Initialize database
docker compose exec backend python init_db.py

# Run migrations
docker compose exec backend python migrate_db.py
```

### With Custom Environment:
```bash
# Set custom database URL
docker compose exec backend bash -c "DATABASE_URL=postgresql://user:pass@host:5432/db python init_db.py"
```

## Troubleshooting

### Common Issues:

1. **Connection Error**:
   - Verify database is running
   - Check connection string format
   - Ensure network connectivity (for remote databases)

2. **Permission Error**:
   - Check database user permissions
   - Verify database exists
   - Ensure user has CREATE privileges

3. **Table Already Exists**:
   - Scripts are idempotent (safe to run multiple times)
   - Use `migrate_db.py` for schema updates

### Logs:
All scripts provide detailed logging. Check console output for error details.

## Database Schema

### Tables Created:
- `users`: User accounts and authentication
- `conversations`: Chat conversations
- `chat_messages`: Individual chat messages
- `tokens`: Authentication tokens
- `schema_version`: Migration tracking

### Indexes:
- `idx_conversations_user_id`: Performance for user queries
- `idx_chat_messages_conversation_id`: Performance for conversation queries
- `idx_chat_messages_timestamp`: Performance for time-based queries

## Security Notes

- Never commit `.env` files with real credentials
- Use strong passwords for production databases
- Consider using connection pooling for production
- Regularly backup your database
- Use SSL connections for remote databases in production 