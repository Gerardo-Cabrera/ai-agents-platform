# Development Guide

This guide provides detailed instructions for setting up and developing the AI Agents System locally.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.10+ (for backend development)
- Git

### One-Command Setup
```bash
# Clone and start everything
git clone <repository-url>
cd agent_ia
./scripts/up_all.sh
```

## 🛠️ Development Environment Setup

### Option 1: Full Docker Development (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent_ia
   ```

2. **Configure development overrides**
   ```bash
   cp docker-compose.override.example.yml docker-compose.override.yml
   # Edit docker-compose.override.yml as needed
   ```

3. **Start development environment**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Monitoring: http://localhost:9090 (Prometheus)

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with backend URL

# Start development server
npm run dev
```

## 🔧 Development Tools

### Code Quality Tools

#### Backend (Python)
```bash
# Format code
black .
isort .

# Lint code
flake8
mypy .

# Run tests
pytest
pytest --cov=app --cov-report=html

# Type checking
mypy app/
```

#### Frontend (JavaScript/React)
```bash
# Format and lint
npm run lint
npm run lint:fix

# Run tests
npm test
npm run test:coverage

# Type checking (if using TypeScript)
npm run type-check
```

### Database Management

#### PostgreSQL (Local)
```bash
# Connect to database
psql -U neo -d agent_user_ai

# Run migrations
python migrate_db.py

# Reset database
python setup_database.py --reset
```

#### SQLite (Development)
```bash
# The system will automatically use SQLite if PostgreSQL is not available
# Database file: backend/agent_ia.db
```

### AI Model Management

#### Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull required models
ollama pull deepseek-coder:6.7b
ollama pull llama2:7b

# List available models
ollama list
```

#### Model Configuration
```bash
# Check model health
curl http://localhost:8000/api/v1/ai/health

# List available models
curl http://localhost:8000/api/v1/ai/models
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run integration tests
pytest tests/integration/
```

### Frontend Testing
```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- --testPathPattern=LoginForm

# Run in watch mode
npm test -- --watch
```

### End-to-End Testing
```bash
# Start the full system
./scripts/up_all.sh

# Run system tests
python tests/system_test.py

# Test API endpoints
curl -X GET http://localhost:8000/health
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "test123", "full_name": "Test User"}'
```

## 🔍 Debugging

### Backend Debugging
```bash
# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start with debugger
python -m pdb -m uvicorn app.main:app --reload

# Use logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Frontend Debugging
```bash
# Enable debug mode
export VITE_DEBUG=true

# Use browser dev tools
# - Network tab for API calls
# - Console for JavaScript errors
# - React DevTools for component debugging
```

### Docker Debugging
```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Enter container
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container status
docker-compose ps
```

## 📊 Monitoring and Logs

### Application Logs
```bash
# View application logs
tail -f backend/logs/app.log

# View Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Performance Monitoring
```bash
# Access Prometheus metrics
curl http://localhost:8000/metrics

# Access Grafana dashboard
# http://localhost:3000 (admin/admin)
```

### Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/api/v1/health/status

# AI service health
curl http://localhost:8000/api/v1/ai/health
```

## 🚀 Deployment Preparation

### Production Build
```bash
# Backend production build
cd backend
docker build -t agent-ia-backend:latest .

# Frontend production build
cd frontend
npm run build
docker build -t agent-ia-frontend:latest .
```

### Environment Configuration
```bash
# Production environment
cp backend/.env.example backend/.env.production
cp frontend/.env.example frontend/.env.production

# Edit production configurations
# - Set DEBUG=false
# - Configure production database
# - Set secure SECRET_KEY
# - Configure CORS origins
```

## 🔧 Common Development Tasks

### Adding New API Endpoints
1. Create endpoint in `backend/app/api/v1/endpoints/`
2. Add route to `backend/app/main.py`
3. Create schema in `backend/app/schemas/`
4. Add service logic in `backend/app/services/`
5. Write tests in `backend/tests/`
6. Update API documentation

### Adding New Frontend Components
1. Create component in `frontend/src/components/`
2. Add styles in corresponding `.css` file
3. Import and use in `frontend/src/App.jsx`
4. Add tests in `frontend/tests/`
5. Update documentation

### Database Schema Changes
1. Update models in `backend/app/models/`
2. Create migration script
3. Update `backend/migrate_db.py`
4. Test migration on development database
5. Update documentation

## 🐛 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :5173

# Kill process
sudo kill -9 <PID>

# Use different ports
docker-compose up -p 8001:8000
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U neo -d agent_user_ai -c "SELECT 1;"

# Reset database
python setup_database.py --reset
```

#### Docker Issues
```bash
# Clean up Docker
docker system prune -a
docker volume prune

# Rebuild images
docker-compose build --no-cache
```

#### AI Model Issues
```bash
# Check Ollama status
ollama list
ollama pull deepseek-coder:6.7b

# Test AI service
curl http://localhost:8000/api/v1/ai/health
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Material-UI Documentation](https://mui.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Ollama Documentation](https://ollama.ai/docs)

## 🤝 Getting Help

- Check the [Troubleshooting](../README.md#-troubleshooting) section
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- Open an issue on GitHub
- Contact the maintainers

---

Happy coding! 🚀 