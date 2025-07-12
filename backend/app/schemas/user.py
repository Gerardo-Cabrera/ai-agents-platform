from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = False

class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: str
