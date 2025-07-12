# Secrets Management Guide

This guide covers how to properly manage secrets and environment variables for your AI Agents System.

## Overview

Secrets management is crucial for security. Never commit sensitive information like API keys, passwords, or tokens to your Git repository.

## Environment Variables Structure

### Backend Environment Variables

Create a `.env` file in your backend directory (never commit this file):

```bash
# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
APP_NAME=AI Agents System
VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
# Generate a secure secret key: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# Local development
DATABASE_URL=sqlite:///./app.db

# Production (PostgreSQL)
# DATABASE_URL=postgresql://username:password@host:port/database

# =============================================================================
# FILE UPLOAD SETTINGS
# =============================================================================
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
TEMP_DIR=temp

# =============================================================================
# EVENT MANAGEMENT
# =============================================================================
EVENT_RETENTION_DAYS=30

# =============================================================================
# LLM API KEYS (CRITICAL - KEEP SECURE)
# =============================================================================

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4096
OPENAI_TEMPERATURE=0.7

# Hugging Face Configuration
HF_API_KEY=hf-your-huggingface-api-key-here
HF_MODEL=meta-llama/Llama-2-7b-chat-hf
HF_MAX_LENGTH=2048
HF_TEMPERATURE=0.7

# DeepSeek Configuration
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=4096
DEEPSEEK_TEMPERATURE=0.7

# Main LLM Configuration
LLM_MAIN=openai

# =============================================================================
# CORS CONFIGURATION
# =============================================================================
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173", "https://your-domain.com"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
ALLOWED_HEADERS=["*"]

# =============================================================================
# MONITORING AND LOGGING
# =============================================================================
SENTRY_DSN=your-sentry-dsn-here  # Optional: for error tracking
LOG_LEVEL=INFO
```

### Frontend Environment Variables

Create a `.env` file in your frontend directory:

```bash
# =============================================================================
# API CONFIGURATION
# =============================================================================
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
VITE_APP_NAME=AI Agents System
VITE_APP_VERSION=1.0.0

# =============================================================================
# FEATURE FLAGS
# =============================================================================
VITE_ENABLE_AUDIO=true
VITE_ENABLE_FILE_UPLOAD=true
VITE_ENABLE_WEBSOCKET=true

# =============================================================================
# ANALYTICS (Optional)
# =============================================================================
VITE_GOOGLE_ANALYTICS_ID=your-ga-id-here
VITE_MIXPANEL_TOKEN=your-mixpanel-token-here
```

## Getting API Keys

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Store it securely

### Hugging Face API Key

1. Go to [Hugging Face](https://huggingface.co/)
2. Sign up or log in
3. Go to "Settings" → "Access Tokens"
4. Click "New token"
5. Give it a name and select permissions
6. Copy the token (starts with `hf_`)
7. Store it securely

### DeepSeek API Key

1. Go to [DeepSeek](https://platform.deepseek.com/)
2. Sign up or log in
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key
6. Store it securely

## Security Best Practices

### 1. Never Commit Secrets

Add these files to your `.gitignore`:

```gitignore
# Environment files
.env
.env.local
.env.production
.env.staging

# Secrets
*.key
*.pem
*.p12
*.pfx

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Temporary files
temp/
tmp/
uploads/
```

### 2. Use Strong Secret Keys

Generate secure secret keys:

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### 3. Rotate Keys Regularly

- Change API keys every 90 days
- Monitor API usage for unusual activity
- Use different keys for different environments

### 4. Environment-Specific Configuration

Create different `.env` files for different environments:

```bash
# Development
.env.development

# Staging
.env.staging

# Production
.env.production
```

## Local Development Setup

### 1. Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your actual values
```

### 2. Frontend Setup

```bash
cd frontend
cp .env.example .env
# Edit .env with your actual values
```

### 3. Verify Configuration

```bash
# Backend
cd backend
python -c "from app.core.config import settings; print('Backend config loaded successfully')"

# Frontend
cd frontend
npm run dev
```

## Production Deployment

### Railway Deployment

1. Go to your Railway project
2. Navigate to "Variables" tab
3. Add each environment variable from the backend list above
4. Ensure all API keys are set correctly

### Docker Deployment

Create a `docker-compose.prod.yml`:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - HF_API_KEY=${HF_API_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      # ... other variables
    env_file:
      - .env.production

  frontend:
    build: ./frontend
    environment:
      - VITE_API_URL=${VITE_API_URL}
      - VITE_WS_URL=${VITE_WS_URL}
    env_file:
      - .env.production
```

## Monitoring and Alerts

### 1. API Usage Monitoring

Set up alerts for:
- High API usage
- Failed API calls
- Rate limit exceeded

### 2. Security Monitoring

Monitor for:
- Unusual login patterns
- Failed authentication attempts
- Suspicious API usage

### 3. Cost Monitoring

Track API costs:
- OpenAI: Monitor usage in OpenAI dashboard
- Hugging Face: Check usage in HF dashboard
- DeepSeek: Monitor in DeepSeek dashboard

## Emergency Procedures

### 1. Key Compromise

If a key is compromised:

1. **Immediately revoke the key** in the provider's dashboard
2. **Generate a new key**
3. **Update all environments** with the new key
4. **Check logs** for unauthorized usage
5. **Notify team members** of the change

### 2. Environment Variable Leak

If environment variables are accidentally committed:

1. **Immediately remove from Git history**:
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all
   ```
2. **Rotate all exposed keys**
3. **Update all environments**
4. **Review access logs**

## Validation Scripts

### Backend Validation

Create a validation script:

```python
# scripts/validate_env.py
import os
from app.core.config import settings

def validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = [
        'SECRET_KEY',
        'OPENAI_API_KEY',
        'HF_API_KEY',
        'DEEPSEEK_API_KEY',
        'LLM_MAIN'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(settings, var, None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return False
    
    print("✅ All required environment variables are set")
    return True

if __name__ == "__main__":
    validate_environment()
```

### Frontend Validation

Create a validation script:

```javascript
// scripts/validate-env.js
const requiredVars = [
  'VITE_API_URL',
  'VITE_WS_URL',
  'VITE_APP_NAME'
];

function validateEnvironment() {
  const missingVars = requiredVars.filter(varName => !import.meta.env[varName]);
  
  if (missingVars.length > 0) {
    console.error('❌ Missing required environment variables:', missingVars);
    process.exit(1);
  }
  
  console.log('✅ All required environment variables are set');
}

validateEnvironment();
```

## Checklist

### Before Deployment

- [ ] All API keys are set and valid
- [ ] Secret key is strong and unique
- [ ] CORS origins are configured correctly
- [ ] Database URL is set
- [ ] File upload directories exist
- [ ] Log directories are created
- [ ] Environment variables are validated

### After Deployment

- [ ] Health endpoints respond correctly
- [ ] API endpoints work with authentication
- [ ] WebSocket connections work
- [ ] File uploads work
- [ ] Logs are being generated
- [ ] Monitoring is set up
- [ ] Alerts are configured

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Hugging Face API Documentation](https://huggingface.co/docs/api-inference)
- [DeepSeek API Documentation](https://platform.deepseek.com/docs)
- [Railway Environment Variables](https://docs.railway.app/develop/variables)
- [Docker Environment Variables](https://docs.docker.com/compose/environment-variables/) 