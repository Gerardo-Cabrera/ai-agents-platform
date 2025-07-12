"""
AI service endpoints with DeepSeek/Ollama integration
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from pydantic import BaseModel
from app.services.ai_service import ai_service
from app.services.auth_service import get_current_user
from app.schemas.user import User

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "deepseek-coder:14b"

class PullModelRequest(BaseModel):
    model_name: str

@router.get("/health")
async def check_ai_health():
    """Check AI service status"""
    return await ai_service.check_ollama_health()

@router.get("/models")
async def list_models(current_user: User = Depends(get_current_user)):
    """List available models in Ollama"""
    result = await ai_service.list_models()
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/generate")
async def generate_response(
    request: GenerateRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate response using the specified model"""
    result = await ai_service.generate_response(
        prompt=request.prompt,
        model=request.model
    )
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/pull-model")
async def pull_model(
    request: PullModelRequest,
    current_user: User = Depends(get_current_user)
):
    """Download a specific model"""
    result = await ai_service.pull_model(request.model_name)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/chat")
async def chat_with_ai(
    request: GenerateRequest,
    current_user: User = Depends(get_current_user)
):
    """Simplified chat with AI model"""
    # Add user context to prompt
    enhanced_prompt = f"""
User: {current_user.username}
Prompt: {request.prompt}

Please provide a helpful and detailed response:
"""
    
    result = await ai_service.generate_response(
        prompt=enhanced_prompt,
        model=request.model
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return {
        "user": current_user.username,
        "prompt": request.prompt,
        "response": result["response"],
        "model": result["model"]
    }
