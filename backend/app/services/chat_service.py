import uuid
import time
import logging
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.chat import (
    ChatRequest, ChatResponse, ChatMessage as ChatMessageSchema, Conversation as ConversationSchema,
    MessageType, WebSocketMessage
)
from app.core.websocket_manager import manager
from app.core.dependencies import get_db
from app.models.conversation import Conversation
from app.models.chat_message import ChatMessage, MessageTypeEnum
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.config import settings
import json

logger = logging.getLogger(__name__)

# LangChain and Ollama modern
try:
    from langchain_ollama import OllamaLLM
    langchain_available = True
except ImportError:
    langchain_available = False
    OllamaLLM = None

# langdetect for multilingual fallback
try:
    from langdetect import detect
except ImportError:
    detect = None

SERVICE_UNAVAILABLE_MESSAGES = {
    'es': 'Por el momento el servicio no está disponible.',
    'en': 'The service is currently unavailable.',
    'fr': 'Le service est actuellement indisponible.',
    'de': 'Der Dienst ist derzeit nicht verfügbar.',
    'pt': 'O serviço não está disponível no momento.',
    'it': 'Il servizio non è disponibile al momento.',
    'default': 'The service is currently unavailable.'
}

def get_unavailable_message(text: str) -> str:
    # Always return the translation key for consistent frontend translation
    return 'serviceUnavailable'

class ChatService:
    """Service for handling chat and conversations, using LangChain+Ollama DeepSeek if available."""
    def __init__(self):
        self.available_models = []
        self.default_model = None
        self.ollama_base_url = settings.ollama_base_url
        
        # Detect available models
        self._detect_available_models()
        
        if langchain_available and self.default_model:
            try:
                self.llm = OllamaLLM(model=self.default_model, base_url=self.ollama_base_url)
                logger.info(f"Successfully initialized {self.default_model} model")
            except Exception as e:
                logger.error(f"OllamaLLM/LangChain initialization error: {e}")
                logger.error("Make sure Ollama is running and the model is downloaded")
                self.llm = None
        else:
            logger.warning("LangChain Ollama not available or no models found. Install with: pip install langchain-ollama")
            self.llm = None

    def _detect_available_models(self):
        """Detect available models in Ollama and set the best one as default."""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json().get("models", [])
                self.available_models = [model["name"] for model in models_data]
                
                # Prioritize models by preference order
                preferred_models = [
                    "deepseek-coder:14b",
                    "deepseek-coder:6.7b", 
                    "deepseek-chat:6.7b",
                    "llama2:7b",
                    "llama2:13b",
                    "mistral:7b",
                    "codellama:7b"
                ]
                
                # Find the first preferred model that is available
                for preferred in preferred_models:
                    if preferred in self.available_models:
                        self.default_model = preferred
                        logger.info(f"Selected default model: {self.default_model}")
                        break
                
                # If no preferred models, use the first available
                if not self.default_model and self.available_models:
                    self.default_model = self.available_models[0]
                    logger.info(f"No preferred model found, using: {self.default_model}")
                
                logger.info(f"Available models: {self.available_models}")
            else:
                logger.error(f"Failed to get models from Ollama: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"Error detecting available models: {e}")
            self.available_models = []
            self.default_model = None

    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        return self.available_models

    def get_default_model(self) -> Optional[str]:
        """Get the current default model."""
        return self.default_model

    async def process_chat_message(self, request: ChatRequest, user_id: int, db: Session = Depends(get_db)) -> ChatResponse:
        start_time = time.time()
        try:
            # Use automatically detected model if none specified
            if not request.model:
                request.model = self.default_model or settings.ollama_default_model
            
            conversation_id = request.conversation_id or str(uuid.uuid4())
            conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id, is_active=True).first()
            if not conversation:
                conversation = Conversation(
                    id=conversation_id,
                    user_id=user_id,
                    title=request.message[:50] + "..." if len(request.message) > 50 else request.message,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    message_count=0,
                    is_active=True
                )
                db.add(conversation)
                db.commit()
            user_message = ChatMessage(
                conversation_id=conversation_id,
                content=request.message,
                message_type=MessageTypeEnum.USER,
                user_id=user_id,
                timestamp=datetime.utcnow(),
                is_active=True
            )
            db.add(user_message)
            db.commit()
            assistant_response = await self._generate_response(request, conversation_id)
            assistant_message = ChatMessage(
                conversation_id=conversation_id,
                content=assistant_response,
                message_type=MessageTypeEnum.ASSISTANT,
                user_id=None,
                timestamp=datetime.utcnow(),
                is_active=True
            )
            db.add(assistant_message)
            conversation.message_count = db.query(ChatMessage).filter_by(conversation_id=conversation_id, is_active=True).count()
            conversation.updated_at = datetime.utcnow()
            db.commit()
            processing_time = time.time() - start_time
            await self._broadcast_message(conversation_id, assistant_response, user_id)
            return ChatResponse(
                response=assistant_response,
                conversation_id=conversation_id,
                model_used=request.model,
                processing_time=processing_time,
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            raise

    async def _generate_response(self, request: ChatRequest, conversation_id: str) -> str:
        """Generates a response using DeepSeek local via LangChain+OllamaLLM, else returns a multilingual unavailable message."""
        if langchain_available and self.llm is not None:
            try:
                prompt = request.message
                result = self.llm.invoke(prompt)
                return result
            except Exception as e:
                logger.error(f"LangChain/OllamaLLM error: {e}")
                return get_unavailable_message(request.message)
        return get_unavailable_message(request.message)

    async def _broadcast_message(self, conversation_id: str, message: str, user_id: int):
        try:
            ws_message = WebSocketMessage(
                type="chat_message",
                data={
                    "conversation_id": conversation_id,
                    "message": message,
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            await manager.broadcast_to_channel(
                ws_message.dict(),
                "chat"
            )
        except Exception as e:
            logger.error(f"Error sending message via WebSocket: {e}")

    def get_conversation_history(self, conversation_id: str, db: Session) -> List[ChatMessageSchema]:
        messages = db.query(ChatMessage).filter_by(conversation_id=conversation_id, is_active=True).order_by(ChatMessage.timestamp.asc()).all()
        return [ChatMessageSchema(
            id=m.id,
            content=m.content,
            message_type=m.message_type.value,
            user_id=m.user_id,
            timestamp=m.timestamp
        ) for m in messages]

    def get_user_conversations(self, user_id: int, db: Session) -> List[ConversationSchema]:
        conversations = db.query(Conversation).filter_by(user_id=user_id, is_active=True).order_by(Conversation.updated_at.desc()).all()
        return [ConversationSchema(
            id=c.id,
            user_id=c.user_id,
            title=c.title,
            created_at=c.created_at,
            updated_at=c.updated_at,
            message_count=c.message_count,
            is_active=c.is_active
        ) for c in conversations]

    def delete_conversation(self, conversation_id: str, user_id: int, db: Session) -> bool:
        conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id, is_active=True).first()
        if conversation:
            conversation.is_active = False
            db.query(ChatMessage).filter_by(conversation_id=conversation_id).update({"is_active": False})
            db.commit()
            return True
        return False

    def get_conversation_stats(self) -> Dict[str, Any]:
        total_conversations = len(self.conversations)
        total_messages = sum(len(messages) for messages in self.messages.values())
        active_conversations = sum(1 for conv in self.conversations.values() if conv.is_active)
        return {
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "total_messages": total_messages,
            "average_messages_per_conversation": total_messages / total_conversations if total_conversations > 0 else 0
        }

    def rename_conversation(self, conversation_id: str, user_id: int, new_title: str, db: Session) -> bool:
        """Renames a conversation if the user is the owner."""
        conversation = db.query(Conversation).filter_by(id=conversation_id, user_id=user_id, is_active=True).first()
        if conversation:
            conversation.title = new_title
            conversation.updated_at = datetime.utcnow()
            db.commit()
            return True
        return False

# Global instance of chat service
chat_service = ChatService()
