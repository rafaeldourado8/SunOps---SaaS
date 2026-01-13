from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

class RegisterDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=3)

class LoginDTO(BaseModel):
    username: str  # Aceita email ou username
    password: str

class TokenDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserDTO(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
