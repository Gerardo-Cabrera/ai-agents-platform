from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from app.schemas.token import Token
from app.schemas.user import User, UserCreate
from app.services.auth_service import (
    authenticate_user, authenticate_user_fallback, create_access_token, 
    create_refresh_token, get_current_user, create_user, get_user_by_username, 
    get_user_by_email, fake_user_db
)
from app.core.database import get_db
from app.models.user import User as UserModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Try database authentication first
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        # Fallback to demo user
        user = authenticate_user_fallback(form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str):
    # Here you should validate the refresh_token and issue a new one
    # Simplified logic for example
    username = "demo_user"  # Extract from refresh_token in real implementation
    access_token = create_access_token(username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/signup", response_model=User)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists in database
    if get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if user exists in fake_user_db (for demo user)
    if user_data.username in fake_user_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create new user in database
    db_user = create_user(db, user_data)
    
    return User(
        username=db_user.username,
        full_name=db_user.full_name,
        email=db_user.email,
        disabled=not db_user.is_active
    )

@router.get("/users", response_model=List[User])
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get users from database
    db_users = db.query(UserModel).all()
    users = []
    
    for db_user in db_users:
        users.append(User(
            username=db_user.username,
            full_name=db_user.full_name,
            email=db_user.email,
            disabled=not db_user.is_active
        ))
    
    # Add demo user from fake_user_db
    for user_data in fake_user_db.values():
        users.append(User(**user_data))
    
    return users 