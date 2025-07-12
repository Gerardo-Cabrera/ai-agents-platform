from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pydantic import SecretStr, validator

class Settings(BaseSettings):
    """
    Main application configuration.
    Critical variables must be defined by the user in production:
    - secret_key
    - log_file
    - upload_dir
    - database_url
    """
    # Basic configuration
    app_name: str = "AI Agents System"
    version: str = "1.0.0"
    debug: bool = False
    
    # Database configuration
    database_url: str = os.getenv('DATABASE_URL')  # Set in .env, e.g. postgresql://user:password@host:port/dbname
    database_echo: bool = False
    
    # Ollama configuration
    ollama_base_url: str = os.getenv('OLLAMA_BASE_URL', 'http://172.17.0.1:11434')  # Set in .env, e.g. http://localhost:11434
    ollama_default_model: str = os.getenv('OLLAMA_DEFAULT_MODEL', 'deepseek-coder:6.7b')  # Default model to use
    
    # Security configuration
    secret_key: SecretStr = SecretStr("your_very_secure_secret_key_here_change_in_production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS configuration
    frontend_origin: Optional[str] = os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')
    allowed_origins: List[str] = []
    allowed_methods: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: list = ["*"]
    
    # WebSocket configuration
    websocket_ping_interval: int = 20
    websocket_ping_timeout: int = 20
    
    # Redis configuration (for Celery and cache)
    redis_url: str = "redis://localhost:6379"
    
    # LLM configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    default_llm_provider: str = "openai"
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # File configuration
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Monitoring and logging
    sentry_dsn: Optional[str] = None
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # Additional configuration fields
    temp_dir: str = "temp"
    event_retention_days: int = 30
    
    # LLM configuration details
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 4096
    openai_temperature: float = 0.7
    
    hf_api_key: Optional[str] = None
    hf_model: str = "meta-llama/Llama-2-7b-chat-hf"
    hf_max_length: int = 2048
    hf_temperature: float = 0.7
    
    deepseek_api_key: Optional[str] = None
    deepseek_model: str = "deepseek-chat"
    deepseek_max_tokens: int = 4096
    deepseek_temperature: float = 0.7
    
    llm_main: str = "openai"
    
    # WebSocket additional configuration
    ws_heartbeat_interval: int = 30
    ws_max_connections: int = 1000
    
    # Redis additional configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # Email configuration
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    def __init__(self, **values):
        super().__init__(**values)
        # Populate allowed_origins from frontend_origin if set
        if self.frontend_origin:
            self.allowed_origins = [self.frontend_origin]

    @validator('log_file', pre=True, always=True)
    def validate_log_file(cls, v):
        """Validate that log_file is not empty."""
        return v or "logs/app.log"

    @validator('upload_dir', pre=True, always=True)
    def validate_upload_dir(cls, v):
        """Validate that upload_dir is not empty."""
        return v or "uploads"
    
    def required_vars(self):
        """Returns critical variables required for production."""
        return {
            'secret_key': self.secret_key.get_secret_value(),
            'log_file': self.log_file,
            'upload_dir': self.upload_dir,
            'database_url': self.database_url
        }
    
    def validate_critical_vars(self):
        """Validates that critical variables don't have insecure values in production."""
        import logging
        if not self.debug:
            if self.secret_key.get_secret_value() == "your_very_secure_secret_key_here_change_in_production":
                raise ValueError(
                    "[SECURITY ERROR] You are using the default secret key in production! "
                    "Set a strong SECRET_KEY in your .env or environment variables.\n"
                    "Example: SECRET_KEY=your_random_generated_secret_here"
                )
            if not self.log_file:
                logging.warning("log_file is empty. It's recommended to define a log file in production.")
            if not self.upload_dir:
                logging.warning("upload_dir is empty. It's recommended to define an uploads directory in production.")
            if self.database_url.startswith("sqlite"):
                logging.warning("You are using SQLite in production. Consider using a more robust database.")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra variables in .env

# Instancia global de configuración
settings = Settings()
settings.validate_critical_vars()

# Crear directorios necesarios
os.makedirs("logs", exist_ok=True)
os.makedirs(settings.upload_dir, exist_ok=True)
