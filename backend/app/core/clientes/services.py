from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete # <-- Importar delete
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

# --- NOVAS FUNÇÕES ADICIONADAS ---

async def update_cliente(
    db: AsyncSession, 
    cliente: models.Cliente, 
    update_data: schema.ClienteUpdate
) -> models.Cliente:
    '''Atualiza um cliente no banco'''
    
    # Pega os dados do schema que foram enviados (excluindo os não definidos)
    data = update_data.model_dump(exclude_unset=True)
    
    # Atualiza os campos do objeto 'cliente'
    for key, value in data.items():
        setattr(cliente, key, value)
        
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    return cliente


async def delete_clientes_bulk(db: AsyncSession, cliente_ids: List[int]) -> int:
    '''Deleta múltiplos clientes pelo ID'''
    
    query = (
        delete(models.Cliente)
        .where(models.Cliente.id.in_(cliente_ids))
    )
    result = await db.execute(query)
    await db.commit()
    
    # Retorna o número de linhas afetadas (quantos foram deletados)
    return result.rowcount