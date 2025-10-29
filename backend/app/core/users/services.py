from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from . import models, schema, hashing

async def create_new_user(
    request: schema.UserCreate, 
    database: AsyncSession
) -> models.User:
    '''Cria um novo usuário no banco com senha hasheada e role'''
    
    hashed_password = hashing.get_password_hash(request.password)
    
    new_user = models.User(
        name=request.name,
        email=request.email,
        password_hash=hashed_password,
        role=request.role  # Define o role vindo do request
    )
    
    database.add(new_user)
    await database.commit()
    await database.refresh(new_user)
    return new_user

async def get_user_by_email(email: str, database: AsyncSession) -> Optional[models.User]:
    '''Busca um usuário pelo email'''
    query = select(models.User).where(models.User.email == email)
    result = await database.execute(query)
    return result.scalars().first()

async def get_user_by_id(user_id: int, database: AsyncSession) -> Optional[models.User]:
    '''Busca um usuário pelo ID'''
    query = select(models.User).where(models.User.id == user_id)
    result = await database.execute(query)
    return result.scalars().first()

async def get_all_users(database: AsyncSession) -> List[models.User]:
    '''Lista todos os usuários (para Gestores)'''
    query = select(models.User)
    result = await database.execute(query)
    return result.scalars().all()

async def delete_user(user: models.User, database: AsyncSession) -> None:
    '''Deleta um usuário (recebe o objeto User)'''
    await database.delete(user)
    await database.commit()