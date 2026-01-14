from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shared.infrastructure.auth.jwt_handler import create_access_token, verify_password
from shared.infrastructure.auth.dependencies import get_current_user
from django.contrib.auth.models import User
router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    try:
        user = User.objects.get(username=request.username)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "role": "ADMIN"
    }
    
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": "ADMIN"
        }
    }


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
