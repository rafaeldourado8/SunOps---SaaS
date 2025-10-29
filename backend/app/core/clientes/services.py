from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List, Optional

from . import models, schema

async def create_new_cliente(
    db: AsyncSession, 
    cliente: schema.ClienteCreate
) -> models.Cliente:
    '''Cria um novo cliente no banco'''
    
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente

async def get_cliente_by_id(db: AsyncSession, cliente_id: int) -> Optional[models.Cliente]:
    '''Busca um cliente específico pelo ID'''
    query = select(models.Cliente).where(models.Cliente.id == cliente_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_cliente_by_documento(db: AsyncSession, documento: str) -> Optional[models.Cliente]:
    '''Verifica se um cliente já existe pelo documento (CPF/CNPJ)'''
    query = select(models.Cliente).where(models.Cliente.documento == documento)
    result = await db.execute(query)
    return result.scalars().first()

async def get_all_clientes(db: AsyncSession) -> List[models.Cliente]:
    '''Lista todos os clientes'''
    query = select(models.Cliente).order_by(models.Cliente.nome_razao_social)
    result = await db.execute(query)
    return result.scalars().all()

async def search_clientes(db: AsyncSession, q: str) -> List[models.Cliente]:
    '''Busca clientes pelo nome (para a barra "Buscar clientes...")'''
    query = (
        select(models.Cliente)
        .where(models.Cliente.nome_razao_social.ilike(f"%{q}%")) # 'ilike' é case-insensitive
        .order_by(models.Cliente.nome_razao_social)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def delete_cliente(db: AsyncSession, cliente: models.Cliente) -> None:
    '''Deleta um cliente'''
    await db.delete(cliente)
    await db.commit()