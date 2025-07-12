# Sistema de Agentes IA - Backend

## Descripción

Backend de FastAPI para el sistema de agentes IA que proporciona APIs para chat, análisis de datos y autenticación con soporte para WebSockets en tiempo real.

## Características

- **FastAPI** - Framework web moderno y rápido
- **Autenticación JWT** - Sistema seguro de autenticación
- **WebSockets** - Comunicación en tiempo real
- **Análisis de Datos** - Integración con LLMs para análisis
- **Base de Datos** - SQLAlchemy con soporte para múltiples bases de datos
- **Documentación Automática** - Swagger/OpenAPI integrado

## Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd agent_ia/backend
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar la aplicación:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Estructura del Proyecto

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py          # Endpoints de autenticación
│   │           ├── chat.py          # Endpoints de chat
│   │           └── data.py          # Endpoints de análisis de datos
│   ├── core/
│   │   ├── config.py               # Configuración de la aplicación
│   │   ├── dependencies.py         # Dependencias de FastAPI
│   │   ├── security.py             # Autenticación y seguridad
│   │   └── websocket_manager.py    # Gestión de WebSockets
│   ├── models/
│   │   ├── user.py                 # Modelo de usuario
│   │   └── token.py                # Modelo de token
│   ├── schemas/
│   │   ├── chat.py                 # Esquemas de chat
│   │   ├── data.py                 # Esquemas de análisis de datos
│   │   └── user.py                 # Esquemas de usuario
│   ├── services/
│   │   ├── auth_service.py         # Servicio de autenticación
│   │   ├── chat_service.py         # Servicio de chat
│   │   └── data_service.py         # Servicio de análisis de datos
│   └── main.py                     # Punto de entrada de la aplicación
├── requirements.txt                # Dependencias de Python
├── Dockerfile                      # Configuración de Docker
└── README.md                       # Este archivo
```

## API Endpoints

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrarse
- `GET /api/v1/auth/me` - Obtener información del usuario actual
- `POST /api/v1/auth/refresh` - Renovar token

### Chat
- `POST /api/v1/chat/message` - Enviar mensaje de chat
- `GET /api/v1/chat/conversations` - Obtener conversaciones del usuario
- `GET /api/v1/chat/conversations/{id}/history` - Obtener historial de conversación
- `DELETE /api/v1/chat/conversations/{id}` - Eliminar conversación

### Análisis de Datos
- `POST /api/v1/data/analyze` - Realizar análisis de datos
- `POST /api/v1/data/upload` - Subir archivo de datos
- `GET /api/v1/data/sources` - Obtener fuentes de datos
- `GET /api/v1/data/analyses` - Obtener historial de análisis

### WebSockets
- `WS /ws/chat` - Canal de chat en tiempo real
- `WS /ws/data` - Canal de análisis de datos en tiempo real
- `WS /ws/notifications` - Canal de notificaciones

## Configuración

### Variables de Entorno

```env
# Configuración básica
APP_NAME=Sistema de Agentes IA
DEBUG=false

# Base de datos
DATABASE_URL=sqlite:///./agent_ia.db

# Seguridad
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# LLM
OPENAI_API_KEY=tu_api_key_de_openai
ANTHROPIC_API_KEY=tu_api_key_de_anthropic
DEFAULT_LLM_PROVIDER=openai

# Redis
REDIS_URL=redis://localhost:6379
```

## Desarrollo

### Ejecutar en modo desarrollo
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar tests
```bash
pytest
```

### Formatear código
```bash
black .
isort .
```

### Linting
```bash
flake8
```

## Docker

### Construir imagen
```bash
docker build -t agent-ia-backend .
```

### Ejecutar contenedor
```bash
docker run -p 8000:8000 agent-ia-backend
```

### Docker Compose
```bash
docker-compose up -d
```

## Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Monitoreo y Logs

Los logs se guardan en `logs/app.log` y incluyen:
- Errores de aplicación
- Conexiones WebSocket
- Análisis de datos
- Autenticación

## Seguridad

- Autenticación JWT con tokens de acceso y refresh
- Hash de contraseñas con bcrypt
- CORS configurado para orígenes específicos
- Validación de entrada con Pydantic
- Rate limiting (configurable)

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
