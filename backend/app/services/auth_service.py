from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas.user import User, UserCreate
from app.core.config import settings
from app.models.user import User as UserModel
from app.core.database import get_db

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy user for backward compatibility
fake_user_db = {
    "demo_user": {
        "username": "demo_user",
        "full_name": "Demo User",
        "email": "demo@example.com",
        "disabled": False,
        "hashed_password": "demo123"  # In real implementation, use hash
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
    """Get user by username from database."""
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """Get user by email from database."""
    return db.query(UserModel).filter(UserModel.email == email).first()

def create_user(db: Session, user_data: UserCreate) -> UserModel:
    """Create a new user in the database."""
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    """Authenticate user with database."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        disabled=not user.is_active
    )

def authenticate_user_fallback(username: str, password: str) -> Optional[User]:
    """Fallback authentication using fake_user_db for demo user."""
    user = fake_user_db.get(username)
    if not user or user["hashed_password"] != password:
        return None
    return User(**user)

def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)

def create_refresh_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Try to get user from database first
    user_model = get_user_by_username(db, username)
    if user_model:
        return User(
            username=user_model.username,
            full_name=user_model.full_name,
            email=user_model.email,
            disabled=not user_model.is_active
        )
    
    # Fallback to fake_user_db for demo user
    user = fake_user_db.get(username)
    if user is None:
        raise credentials_exception
    return User(**user)
