from fastapi import APIRouter
from app.core.config import settings
from app.core.websocket_manager import manager

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.version,
        "database": "connected" if settings.database_url else "not_configured",
        "websocket_connections": manager.get_connection_count()
    }

@router.get("/status")
async def system_status():
    """Detailed system status endpoint."""
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
        "websocket_channels": {
            "chat": manager.get_connection_count("chat"),
            "data": manager.get_connection_count("data"),
            "notifications": manager.get_connection_count("notifications")
        },
        "total_connections": manager.get_connection_count()
    }

@router.get("/info")
async def app_info():
    """Root endpoint with application information."""
    return {
        "message": "AI Agents System",
        "version": settings.version,
        "status": "running",
        "docs": "/docs"
    } 