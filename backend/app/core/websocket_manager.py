from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from app.core.security import verify_token
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Gestor de conexiones WebSocket."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "chat": set(),
            "data": set(),
            "notifications": set()
        }
        self.user_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, channel: str, token: str = None):
        """Conecta un WebSocket a un canal específico."""
        try:
            await websocket.accept()
            
            # Verificar token si se proporciona
            user_id = None
            if token:
                payload = verify_token(token)
                if payload:
                    user_id = payload.get("sub")
            
            # Agregar conexión al canal
            if channel in self.active_connections:
                self.active_connections[channel].add(websocket)
                if user_id:
                    self.user_connections[user_id] = websocket
                
                logger.info(f"Usuario {user_id} conectado al canal {channel}")
                
                # Enviar mensaje de confirmación
                await self.send_personal_message(
                    {"type": "connection", "status": "connected", "channel": channel},
                    websocket
                )
            else:
                await websocket.close(code=4000, reason="Canal no válido")
                
        except Exception as e:
            logger.error(f"Error al conectar WebSocket: {e}")
            await websocket.close(code=4001, reason="Error de conexión")
    
    def disconnect(self, websocket: WebSocket, channel: str):
        """Desconecta un WebSocket de un canal."""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
        
        # Remover de conexiones de usuario
        user_id = None
        for uid, ws in self.user_connections.items():
            if ws == websocket:
                user_id = uid
                break
        
        if user_id:
            del self.user_connections[user_id]
            logger.info(f"Usuario {user_id} desconectado del canal {channel}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Envía un mensaje personal a un WebSocket específico."""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error al enviar mensaje personal: {e}")
    
    async def broadcast_to_channel(self, message: dict, channel: str):
        """Envía un mensaje a todos los WebSockets de un canal."""
        if channel in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[channel]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error al enviar mensaje broadcast: {e}")
                    disconnected.add(connection)
            
            # Limpiar conexiones desconectadas
            for connection in disconnected:
                self.active_connections[channel].discard(connection)
    
    async def send_to_user(self, message: dict, user_id: str):
        """Envía un mensaje a un usuario específico."""
        if user_id in self.user_connections:
            try:
                await self.send_personal_message(message, self.user_connections[user_id])
            except Exception as e:
                logger.error(f"Error al enviar mensaje a usuario {user_id}: {e}")
    
    def get_connection_count(self, channel: str = None) -> int:
        """Obtiene el número de conexiones activas."""
        if channel:
            return len(self.active_connections.get(channel, set()))
        return sum(len(connections) for connections in self.active_connections.values())

# Instancia global del gestor de conexiones
manager = ConnectionManager()

async def get_websocket_manager() -> ConnectionManager:
    """Dependencia para obtener el gestor de WebSockets."""
    return manager
