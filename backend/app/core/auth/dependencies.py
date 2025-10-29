from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.core.users import services as user_services, models
from . import services as auth_services # O arquivo que acabamos de criar

# 1. Define o esquema de autenticação (espera um "Bearer Token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") # Aponta para o seu endpoint de login

# 2. DEPENDÊNCIA BASE: Pega o usuário logado (Autenticação)
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> models.User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
    )
    
    payload = auth_services.decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = await user_services.get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
        
    return user # Retorna o objeto User completo

# 3. DEPENDÊNCIA DE REGRA: Exige ser GESTOR (Autorização)
def get_current_gestor(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    
    if current_user.role != models.UserRole.GESTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso negado. Requer permissão de Gestor."
        )
    return current_user

# 4. DEPENDÊNCIA DE REGRA: Exige ser VENDEDOR (Autorização)
def get_current_vendedor(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    
    if current_user.role != models.UserRole.VENDEDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso negado. Requer permissão de Vendedor."
        )
    return current_user