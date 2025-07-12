# Railway Deployment Guide

This guide will help you deploy your AI Agents System to Railway and configure all necessary secrets.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **API Keys**: You'll need API keys for the LLM services you want to use

## Step 1: Connect Your Repository

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the `railway.json` configuration

## Step 2: Configure Environment Variables

Railway will use the environment variables from your `.env.example` file. You need to set these in the Railway dashboard:

### Required Environment Variables

Go to your project settings in Railway and add these environment variables:

#### Backend Configuration
```bash
# Application Settings
APP_NAME=AI Agents System
VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Security
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (Railway provides PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
TEMP_DIR=temp

# Event Management
EVENT_RETENTION_DAYS=30
```

#### LLM API Keys
```bash
# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4

# Hugging Face
HF_API_KEY=hf-your-huggingface-api-key-here
HF_MODEL=meta-llama/Llama-2-7b-chat-hf

# DeepSeek
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_MODEL=deepseek-chat

# Main LLM Configuration
LLM_MAIN=openai
```

#### CORS Configuration
```bash
# CORS Settings
ALLOWED_ORIGINS=["https://your-frontend-domain.railway.app", "http://localhost:3000"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
ALLOWED_HEADERS=["*"]
```

### How to Set Environment Variables in Railway

1. Go to your Railway project dashboard
2. Click on your service (backend)
3. Go to the "Variables" tab
4. Click "New Variable"
5. Add each variable from the list above
6. Click "Add" to save

## Step 3: Deploy Your Application

Railway will automatically deploy your application when you push to your main branch. The deployment process:

1. **Build Stage**: Railway reads your `railway.json` and builds the Docker image
2. **Deploy Stage**: Deploys the container to Railway's infrastructure
3. **Health Check**: Railway checks if your app responds on the health endpoint

### Monitoring Deployment

1. Go to the "Deployments" tab in your Railway project
2. You can see the build logs and deployment status
3. If there are errors, check the logs for debugging

## Step 4: Configure Custom Domain (Optional)

1. Go to your Railway project settings
2. Click "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

## Step 5: Set Up Frontend Deployment

If you want to deploy the frontend separately:

1. Create a new service in Railway for the frontend
2. Set the build command: `npm run build`
3. Set the start command: `npm start`
4. Configure frontend environment variables:

```bash
# Frontend Environment Variables
VITE_API_URL=https://your-backend-domain.railway.app
VITE_WS_URL=wss://your-backend-domain.railway.app
```

## Step 6: Database Setup

Railway provides PostgreSQL databases:

1. Go to your Railway project
2. Click "New" → "Database" → "PostgreSQL"
3. Railway will automatically set the `DATABASE_URL` environment variable
4. Your app will automatically create tables on first run

## Step 7: Monitoring and Logs

### View Logs
1. Go to your Railway project
2. Click on your service
3. Go to the "Logs" tab
4. You can see real-time application logs

### Health Monitoring
Your app includes health endpoints:
- `GET /health` - Basic health check
- `GET /api/v1/health/` - Detailed health status
- `GET /api/v1/health/status` - System status

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
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

### Debug Mode

For debugging, you can temporarily set:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

This will provide more detailed logs and enable debug endpoints.

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

## Cost Optimization

1. **Free Tier Limits**
   - Railway offers a free tier with usage limits
   - Monitor your usage in the dashboard

2. **Scaling**
   - Railway can auto-scale based on traffic
   - Configure scaling rules as needed

## Next Steps

After deployment:

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

## Example Deployment URLs

After successful deployment, your application will be available at:
- Backend API: `https://your-project-name-production.up.railway.app`
- Frontend: `https://your-frontend-project-name-production.up.railway.app`
- API Documentation: `https://your-project-name-production.up.railway.app/docs` 