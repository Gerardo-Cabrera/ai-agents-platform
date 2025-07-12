from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.models.user import User
import logging

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de seguridad HTTP
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash usando passlib."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña usando passlib."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso con expiración opcional."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verifica y decodifica un token JWT. Devuelve el payload o None si es inválido."""
    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            logging.warning("Token JWT sin 'sub' (username)")
            return None
        return payload
    except JWTError as e:
        logging.error(f"Error decodificando JWT: {e}")
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Obtiene el usuario actual basado en el token JWT. Lanza HTTPException si no es válido."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            logging.warning("Token inválido o expirado")
            raise credentials_exception
        
        username: str = payload.get("sub")
        if username is None:
            logging.warning("Token JWT sin username")
            raise credentials_exception
            
    except JWTError as e:
        logging.error(f"Error de JWT: {e}")
        raise credentials_exception
    
    # Solo para desarrollo: en producción, obtener el usuario real de la base de datos aquí
    user = User(
        id=1,
        username=username,
        email=f"{username}@example.com",
        full_name=username,
        is_active=True
    )
    
    if not user.is_active:
        logging.warning(f"Usuario inactivo: {username}")
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtiene el usuario activo actual. Lanza HTTPException si está inactivo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

def authenticate_user(username: str, password: str, user: User) -> Union[User, bool]:
    """Autentica un usuario con username y password. Devuelve el usuario o False."""
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
