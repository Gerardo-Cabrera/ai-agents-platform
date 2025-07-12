from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """Tipos de mensajes."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ERROR = "error"

class ChatMessage(BaseModel):
    """Esquema para un mensaje de chat."""
    id: Optional[int] = None
    content: str = Field(..., min_length=1, max_length=4000)
    message_type: MessageType = MessageType.USER
    user_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[dict] = None

class ChatRequest(BaseModel):
    """Esquema para solicitud de chat."""
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[str] = None
    model: Optional[str] = None  # Se establecerá dinámicamente basado en modelos disponibles
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(1000, ge=1, le=4000)

class ChatResponse(BaseModel):
    """Esquema para respuesta de chat."""
    response: str
    conversation_id: str
    model_used: str
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Conversation(BaseModel):
    """Esquema para una conversación."""
    id: str
    user_id: int
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    is_active: bool = True

class ConversationList(BaseModel):
    """Esquema para lista de conversaciones."""
    conversations: List[Conversation]
    total: int
    page: int
    per_page: int

class WebSocketMessage(BaseModel):
    """Esquema para mensajes WebSocket."""
    type: str = Field(..., description="Tipo de mensaje")
    data: dict = Field(..., description="Datos del mensaje")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None

class ChatHistoryRequest(BaseModel):
    """Esquema para solicitar historial de chat."""
    conversation_id: str
    limit: Optional[int] = Field(50, ge=1, le=100)
    offset: Optional[int] = Field(0, ge=0)

class ChatHistoryResponse(BaseModel):
    """Esquema para respuesta del historial de chat."""
    messages: List[ChatMessage]
    conversation_id: str
    total_messages: int
    has_more: bool
