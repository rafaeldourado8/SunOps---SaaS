from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# acima realizamos os imports das bibliotecas 
from app.db import get_db
from app.core.auth.dependencies import get_current_user, get_current_gestor # Suas regras de permissão
from . import services, schema, models
# acima realizamos os imports dos modulos 

# criamos a rota do aplicativo com prefixo e tag
router = APIRouter(tags=['Users'], prefix='/users')

# criamos a rota post q envia o status apos criacao da conta
@router.post(
    '/', 
    status_code=status.HTTP_201_CREATED, 
    response_model=schema.ShowUser,
    summary="Cria um novo usuário (Apenas Gestores)"
)

async def create_user(
    request: schema.UserCreate, 
    database: AsyncSession = Depends(get_db),
    # Permissão: Apenas um Gestor logado pode criar novos usuários
    gestor: models.User = Depends(get_current_gestor) 
):
    '''Cria um novo usuário (Vendedor, Gestor, etc.) no sistema.'''
    
    user_exists = await services.get_user_by_email(request.email, database)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O usuário com este email já existe no sistema."
        )
    
    new_user = await services.create_new_user(request, database)
    return new_user


@router.get(
    '/', 
    response_model=List[schema.ShowUser],
    summary="Lista todos os usuários (Apenas Gestores)"
)
async def get_all_users(
    database: AsyncSession = Depends(get_db),
    gestor: models.User = Depends(get_current_gestor)
):
    '''Obtém uma lista de todos os usuários cadastrados no sistema.'''
    users = await services.get_all_users(database)
    return users


@router.get(
    '/me', 
    response_model=schema.ShowUser,
    summary="Retorna os dados do usuário logado"
)
async def get_me(
    # Permissão: Qualquer usuário logado pode ver seus próprios dados
    current_user: models.User = Depends(get_current_user)
):
    '''Retorna os dados do usuário que está atualmente autenticado.'''
    return current_user


@router.get(
    '/{user_id}', 
    response_model=schema.ShowUser,
    summary="Busca um usuário por ID (Apenas Gestores)"
)
async def get_user_by_id(
    user_id: int, 
    database: AsyncSession = Depends(get_db),
    gestor: models.User = Depends(get_current_gestor)
):
    '''Obtém os detalhes de um usuário específico pelo seu ID.'''
    user = await services.get_user_by_id(user_id, database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {user_id} não encontrado."
        )
    return user


@router.delete(
    '/{user_id}', 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um usuário (Apenas Gestores)"
)
async def delete_user_by_id(
    user_id: int, 
    database: AsyncSession = Depends(get_db),
    gestor: models.User = Depends(get_current_gestor)
):
    '''Deleta um usuário do sistema pelo seu ID.'''
    user = await services.get_user_by_id(user_id, database)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {user_id} não encontrado."
        )
    
    await services.delete_user(user, database)
    return Response(status_code=status.HTTP_204_NO_CONTENT)