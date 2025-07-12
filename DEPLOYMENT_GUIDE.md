# AI Agents System - Deployment Guide

This guide will walk you through deploying your AI Agents System to Railway, including both backend and frontend.

## Prerequisites

- [GitHub Account](https://github.com)
- [Railway Account](https://railway.app)
- [OpenAI API Key](https://platform.openai.com/api-keys) (or other LLM provider)
- [Node.js](https://nodejs.org/) (for Railway CLI)

## Step 1: Prepare Your Repository

### 1.1 Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Create repository on GitHub and push
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Repository Structure

Your repository should have this structure:
```
agent_ia/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── railway.json
│   └── env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── env.example
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── README.md
```

## Step 2: Configure Environment Variables

### 2.1 Get API Keys

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

#### Hugging Face API Key (Optional)
1. Go to [Hugging Face](https://huggingface.co/)
2. Sign up or log in
3. Go to "Settings" → "Access Tokens"
4. Click "New token"
5. Copy the token (starts with `hf_`)

#### DeepSeek API Key (Optional)
1. Go to [DeepSeek](https://platform.deepseek.com/)
2. Sign up or log in
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key

### 2.2 Generate Secret Key

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 3: Deploy Backend to Railway

### 3.1 Create Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the `railway.json` configuration

### 3.2 Configure Environment Variables

In your Railway project dashboard:

1. Go to "Variables" tab
2. Add these variables (replace with your actual values):

```bash
# Application Settings
APP_NAME=AI Agents System
VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Security
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
TEMP_DIR=temp

# Event Management
EVENT_RETENTION_DAYS=30

# LLM API Keys
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4096
OPENAI_TEMPERATURE=0.7

HF_API_KEY=hf-your-huggingface-api-key-here
HF_MODEL=meta-llama/Llama-2-7b-chat-hf
HF_MAX_LENGTH=2048
HF_TEMPERATURE=0.7

DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=4096
DEEPSEEK_TEMPERATURE=0.7

LLM_MAIN=openai
DEFAULT_LLM_PROVIDER=openai

# CORS (update with your frontend URL after deployment)
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
ALLOWED_HEADERS=["*"]

# WebSocket
WEBSOCKET_PING_INTERVAL=20
WEBSOCKET_PING_TIMEOUT=20
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=1000

# Database (Railway will provide this automatically)
# DATABASE_URL will be set by Railway

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
```

### 3.3 Add PostgreSQL Database

1. In your Railway project
2. Click "New" → "Database" → "PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable

### 3.4 Deploy Backend

Railway will automatically deploy when you push to your main branch. To deploy manually:

1. Go to "Deployments" tab
2. Click "Deploy Now"
3. Monitor the build logs for any errors

### 3.5 Get Backend URL

1. Go to "Settings" tab
2. Copy the generated domain (e.g., `https://your-project-name-production.up.railway.app`)

## Step 4: Deploy Frontend

### 4.1 Create Frontend Service in Railway

1. In your Railway project
2. Click "New" → "Service" → "GitHub Repo"
3. Select the same repository
4. Set the following configuration:

**Build Command:**
```bash
cd frontend && npm install && npm run build
```

**Start Command:**
```bash
cd frontend && npm start
```

**Root Directory:**
```
frontend
```

### 4.2 Configure Frontend Environment Variables

In the frontend service variables:

```bash
# API Configuration (update with your backend URL)
VITE_API_URL=https://your-backend-project-name-production.up.railway.app
VITE_WS_URL=wss://your-backend-project-name-production.up.railway.app

# Application Settings
VITE_APP_NAME=AI Agents System
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION=Intelligent system with multiple specialized agents

# Feature Flags
VITE_ENABLE_AUDIO=true
VITE_ENABLE_FILE_UPLOAD=true
VITE_ENABLE_WEBSOCKET=true
VITE_ENABLE_AUTONOMOUS_ACTIONS=true
VITE_ENABLE_DATA_ANALYSIS=true

# UI Configuration
VITE_DEFAULT_THEME=light
VITE_ENABLE_DARK_MODE=true
VITE_MAX_FILE_SIZE=10485760
VITE_MAX_MESSAGE_LENGTH=10000
VITE_MAX_OBJECTIVE_LENGTH=5000

# WebSocket Configuration
VITE_WS_RECONNECT_ATTEMPTS=5
VITE_WS_RECONNECT_INTERVAL=3000
VITE_WS_HEARTBEAT_INTERVAL=30000

# API Configuration
VITE_API_TIMEOUT=10000
VITE_API_RETRY_ATTEMPTS=3

# Cache Configuration
VITE_CACHE_TTL=300000
VITE_CACHE_MAX_SIZE=100

# Development Settings
VITE_DEBUG_MODE=false
VITE_LOG_LEVEL=info
VITE_ENABLE_MOCK_DATA=false

# Security
VITE_ENABLE_HTTPS_ONLY=true
VITE_ENABLE_CSP=true
```

### 4.3 Deploy Frontend

1. Railway will automatically deploy when you push to main
2. Monitor the build logs for any errors
3. Get the frontend URL from the service settings

## Step 5: Update CORS Configuration

### 5.1 Update Backend CORS

Once you have both URLs, update the backend CORS configuration:

1. Go to backend service variables
2. Update `ALLOWED_ORIGINS` with your frontend URL:

```bash
ALLOWED_ORIGINS=["https://your-frontend-domain.railway.app", "http://localhost:3000"]
```

3. Redeploy the backend service

## Step 6: Test Your Deployment

### 6.1 Test Backend Endpoints

```bash
# Health check
curl https://your-backend-url.railway.app/health

# API documentation
curl https://your-backend-url.railway.app/docs

# Health status
curl https://your-backend-url.railway.app/api/v1/health/
```

### 6.2 Test Frontend

1. Open your frontend URL in a browser
2. Test the chat functionality
3. Test WebSocket connections
4. Test file uploads
5. Test autonomous actions

### 6.3 Test WebSocket Connections

```javascript
// Test WebSocket connection
const ws = new WebSocket('wss://your-backend-url.railway.app/ws/chat');
ws.onopen = () => console.log('WebSocket connected');
ws.onmessage = (event) => console.log('Message:', event.data);
ws.onerror = (error) => console.error('WebSocket error:', error);
```

## Step 7: Configure Custom Domains (Optional)

### 7.1 Backend Custom Domain

1. Go to backend service settings
2. Click "Domains"
3. Add your custom domain (e.g., `api.yourdomain.com`)
4. Configure DNS records as instructed

### 7.2 Frontend Custom Domain

1. Go to frontend service settings
2. Click "Domains"
3. Add your custom domain (e.g., `app.yourdomain.com`)
4. Configure DNS records as instructed

### 7.3 Update Environment Variables

After setting custom domains, update the environment variables:

**Backend:**
```bash
ALLOWED_ORIGINS=["https://app.yourdomain.com", "https://yourdomain.com"]
```

**Frontend:**
```bash
VITE_API_URL=https://api.yourdomain.com
VITE_WS_URL=wss://api.yourdomain.com
```

## Step 8: Monitoring and Maintenance

### 8.1 Set Up Monitoring

1. **Railway Logs**: Monitor application logs in Railway dashboard
2. **Health Checks**: Use `/health` endpoint for monitoring
3. **Error Tracking**: Consider integrating Sentry for error tracking

### 8.2 Set Up Alerts

1. **Railway Alerts**: Configure alerts for deployment failures
2. **API Monitoring**: Monitor API usage and costs
3. **Performance Monitoring**: Track response times and errors

### 8.3 Backup Strategy

1. **Database Backups**: Railway provides automatic PostgreSQL backups
2. **Code Backups**: Your code is backed up in GitHub
3. **Environment Variables**: Keep a secure backup of your environment variables

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt` (backend) and `package.json` (frontend)
   - Verify Dockerfile syntax
   - Check build logs for specific errors

2. **Environment Variables**
   - Ensure all required variables are set
   - Check for typos in variable names
   - Verify API keys are valid

3. **Database Connection**
   - Verify `DATABASE_URL` is correctly set
   - Check if database service is running
   - Ensure database tables are created

4. **CORS Issues**
   - Update `ALLOWED_ORIGINS` with your frontend URL
   - Check if frontend is making requests to correct backend URL
   - Verify HTTPS/WSS protocols

5. **WebSocket Issues**
   - Check if WebSocket endpoints are accessible
   - Verify CORS configuration for WebSocket
   - Check browser console for connection errors

### Debug Mode

For debugging, temporarily set:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

This will provide more detailed logs and enable debug endpoints.

## Cost Optimization

1. **Free Tier Limits**
   - Railway offers a free tier with usage limits
   - Monitor your usage in the dashboard

2. **API Usage**
   - Monitor LLM API usage and costs
   - Set up usage alerts
   - Consider rate limiting

3. **Scaling**
   - Railway can auto-scale based on traffic
   - Configure scaling rules as needed

## Security Best Practices

1. **Never commit secrets to Git**
   - All sensitive data should be environment variables
   - Use Railway's secret management

2. **Rotate API Keys Regularly**
   - Update your LLM API keys periodically
   - Monitor API usage for unusual activity

3. **Use HTTPS**
   - Railway provides SSL certificates automatically
   - Always use HTTPS in production

4. **Monitor Logs**
   - Regularly check application logs
   - Set up alerts for errors

## Next Steps

After successful deployment:

1. **Test Your Application**
   - Verify all endpoints work
   - Test WebSocket connections
   - Check file upload functionality

2. **Set Up Monitoring**
   - Configure health checks
   - Set up error tracking
   - Monitor performance

3. **CI/CD Integration**
   - Your GitHub Actions workflow will automatically deploy
   - Push to main branch to trigger deployment

4. **Backup Strategy**
   - Railway provides database backups
   - Consider additional backup solutions

## Support

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Use your repository's issue tracker

## Example URLs

After successful deployment, your application will be available at:
- Backend API: `https://your-project-name-production.up.railway.app`
- Frontend: `https://your-frontend-project-name-production.up.railway.app`
- API Documentation: `https://your-project-name-production.up.railway.app/docs` 