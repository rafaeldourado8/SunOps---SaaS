from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.core.users import services as user_services
from . import services as auth_services # <-- (Veja o arquivo 2)

router = APIRouter(tags=['Authentication'], prefix='/auth')

@router.post('/login')
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    # 'OAuth2PasswordRequestForm' força o body a ser 'username' e 'password'
    form_data: OAuth2PasswordRequestForm = Depends() 
):
    # 1. Pega o usuário pelo email (que vem no campo 'username')
    user = await user_services.get_user_by_email(form_data.username, db)

    # 2. Verifica se o usuário existe E se a senha está correta
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Cria o token JWT (passando o 'email' e o 'role' para o token)
    access_token = auth_services.create_access_token(
        data={"sub": user.email, "role": str(user.role.value)} 
    )
    
    return {"access_token": access_token, "token_type": "bearer"}