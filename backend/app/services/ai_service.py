"""
AI Service for DeepSeek/Ollama integration
"""
import os
import json
import requests
from typing import Dict, List, Optional, Any
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaLLM(LLM):
    """Class to interact with local Ollama"""
    
    base_url: str = settings.ollama_base_url
    model: str = settings.ollama_default_model
    temperature: float = 0.7
    max_tokens: int = 2048
    
    @property
    def _llm_type(self) -> str:
        return "ollama"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Execute the Ollama model"""
        try:
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            return f"Error: {str(e)}"

class AIService:
    """Main AI service for the backend"""
    
    def __init__(self):
        self.ollama_base_url = settings.ollama_base_url
        self.llm = OllamaLLM(base_url=self.ollama_base_url)
        
    async def check_ollama_health(self) -> Dict[str, Any]:
        """Check Ollama status"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "status": "healthy",
                    "models": [model["name"] for model in models],
                    "base_url": self.ollama_base_url
                }
            else:
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}",
                    "base_url": self.ollama_base_url
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "base_url": self.ollama_base_url
            }
    
    async def generate_response(self, prompt: str, model: str = None) -> Dict[str, Any]:
        """Generate response using the specified model"""
        try:
            # Update model if different
            if model and model != self.llm.model:
                self.llm.model = model
            
            response = self.llm._call(prompt)
            
            return {
                "success": True,
                "response": response,
                "model": self.llm.model,
                "prompt_length": len(prompt)
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": self.llm.model
            }
    
    async def list_models(self) -> Dict[str, Any]:
        """List available models in Ollama"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            return {
                "success": True,
                "models": [
                    {
                        "name": model["name"],
                        "size": model.get("size", 0),
                        "modified_at": model.get("modified_at", "")
                    }
                    for model in models
                ]
            }
            
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Download a specific model"""
        try:
            url = f"{self.ollama_base_url}/api/pull"
            data = {"name": model_name}
            
            response = requests.post(url, json=data, timeout=300)  # 5 minutes timeout
            response.raise_for_status()
            
            return {
                "success": True,
                "message": f"Model {model_name} pulled successfully",
                "model": model_name
            }
            
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": model_name
            }

# Global service instance
ai_service = AIService()
