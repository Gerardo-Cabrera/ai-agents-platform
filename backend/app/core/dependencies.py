from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from app.core.config import settings
import logging
from app.models.base import Base
from app.models.conversation import Conversation
from app.models.chat_message import ChatMessage

# Configuración de la base de datos
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependencia para obtener la sesión de base de datos (SQLAlchemy)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear las tablas
def create_tables() -> None:
    """Crea todas las tablas en la base de datos."""
    Base.metadata.create_all(bind=engine)

# Función para verificar la conexión a la base de datos
def check_db_connection() -> bool:
    """Verifica la conexión a la base de datos. Devuelve True si es exitosa, False si hay error."""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logging.error(f"Error de conexión a la base de datos: {e}")
        return False
