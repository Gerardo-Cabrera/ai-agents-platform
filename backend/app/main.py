from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os
from logging.handlers import RotatingFileHandler
from prometheus_client import Counter, Gauge
from prometheus_fastapi_instrumentator import Instrumentator

# Sentry integration for production error monitoring
try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False

from app.core.config import settings
from app.core.dependencies import create_tables
from app.core.websocket_manager import manager
from app.api.v1.endpoints import auth, health, chat, ai
from app.utils.celery_metrics import start_queue_length_updater, celery_queue_length

# Configure robust and rotating logging
handlers = []
if getattr(settings, 'log_file', None):
    log_dir = os.path.dirname(settings.log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    try:
        handlers.append(RotatingFileHandler(settings.log_file, maxBytes=5*1024*1024, backupCount=3))
    except Exception as e:
        print(f"[WARN] Could not create FileHandler for logs: {e}. Only StreamHandler will be used.")
handlers.append(logging.StreamHandler())
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
    handlers=handlers
)

# Warning if secret key is the example one in production
if not settings.debug and settings.secret_key.get_secret_value() == "tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion":
    logging.warning("You are using the default secret key in production! Change it immediately.")

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI Agents System with real-time chat and data analysis",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Mount static files
if os.path.exists(settings.upload_dir):
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1/ai")

# Custom Prometheus metrics for AI agents and Celery
ia_responses_total = Counter(
    "ia_responses_total",
    "Total IA agent responses generated",
    ["agent_name", "model"]
)

# Example usage in your code:
# ia_responses_total.labels(agent_name="chatbot", model="gpt-3.5-turbo").inc()

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with application information."""
    return {
        "message": "AI Agents System",
        "version": settings.version,
        "status": "running",
        "docs": "/docs",
        "api": "/api/v1"
    }

# WebSocket endpoints (must be in main.py, not in routers)
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    try:
        await manager.connect(websocket, "chat")
        logger.info("New chat WebSocket connection")
        while True:
            try:
                data = await websocket.receive_text()
                await manager.broadcast_to_channel({"type": "message", "data": data}, "chat")
            except WebSocketDisconnect:
                manager.disconnect(websocket, "chat")
                logger.info("Chat WebSocket connection closed")
                break
    except Exception as e:
        logger.error(f"Error in chat WebSocket: {e}")

@app.websocket("/ws/data")
async def websocket_data(websocket: WebSocket):
    """WebSocket endpoint for real-time data analysis."""
    try:
        await manager.connect(websocket, "data")
        logger.info("New data WebSocket connection")
        while True:
            try:
                data = await websocket.receive_text()
                await manager.broadcast_to_channel({"type": "data_query", "data": data}, "data")
            except WebSocketDisconnect:
                manager.disconnect(websocket, "data")
                logger.info("Data WebSocket connection closed")
                break
    except Exception as e:
        logger.error(f"Error in data WebSocket: {e}")

@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    """WebSocket endpoint for real-time notifications."""
    try:
        await manager.connect(websocket, "notifications")
        logger.info("New notifications WebSocket connection")
        while True:
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                manager.disconnect(websocket, "notifications")
                logger.info("Notifications WebSocket connection closed")
                break
    except Exception as e:
        logger.error(f"Error in notifications WebSocket: {e}")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    # Initialize Sentry for production error monitoring
    if SENTRY_AVAILABLE and settings.sentry_dsn and not settings.debug:
        try:
            sentry_sdk.init(
                dsn=settings.sentry_dsn,
                integrations=[
                    FastApiIntegration(),
                    LoggingIntegration(
                        level=logging.INFO,
                        event_level=logging.ERROR
                    ),
                ],
                traces_sample_rate=0.1,
                environment="production" if not settings.debug else "development"
            )
            logger.info("Sentry error monitoring initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Sentry: {e}")
    
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    try:
        create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    os.makedirs(settings.upload_dir, exist_ok=True)
    log_dir = os.path.dirname(settings.log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    logger.info("Application started successfully")
    start_queue_length_updater(queue_name="celery", interval=10)

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down application...")
    for channel in manager.active_connections:
        for connection in manager.active_connections[channel].copy():
            try:
                await connection.close()
            except:
                pass
    logger.info("Application shut down successfully")

# Force appropriate log level based on environment
if not settings.debug:
    logging.getLogger().setLevel(logging.INFO)

# Security headers middleware
@app.middleware("http")
async def security_headers_middleware(request, call_next):
    response: Response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    return response

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Debug endpoints (only in debug mode)
def include_debug_endpoints(app):
    if settings.debug:
        @app.get("/config/required")
        async def config_required():
            return settings.required_vars()

include_debug_endpoints(app)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

if __name__ == "__main__":
    import uvicorn
    if settings.debug:
        create_tables()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
