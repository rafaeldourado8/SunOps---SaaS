from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List, Optional

from . import models, schema
from app.core.users.models import User

async def create_proposta(
    db: AsyncSession, 
    proposta: schema.PropostaCreate, 
    vendedor_id: int
) -> models.Proposta:
    '''Cria uma nova proposta no banco'''
    
    db_proposta = models.Proposta(
        **proposta.model_dump(),
        vendedor_id=vendedor_id # Associa ao vendedor logado
    )
    db.add(db_proposta)
    await db.commit()
    await db.refresh(db_proposta)
    # Recarrega com os dados do vendedor e cliente para retornar ao frontend
    return await get_proposta_by_id(db, db_proposta.id)

async def get_proposta_by_id(db: AsyncSession, proposta_id: int) -> Optional[models.Proposta]:
    '''Busca uma proposta específica, com dados do cliente e vendedor'''
    query = (
        select(models.Proposta)
        .where(models.Proposta.id == proposta_id)
        .options(
            joinedload(models.Proposta.vendedor_responsavel), # Carrega o User
            joinedload(models.Proposta.cliente)             # Carrega o Cliente
        )
    )
    result = await db.execute(query)
    return result.scalars().first()

async def get_all_propostas(db: AsyncSession) -> List[models.Proposta]:
    '''Lista todas as propostas (para Gestores)'''
    query = (
        select(models.Proposta)
        .options(
            joinedload(models.Proposta.vendedor_responsavel),
            joinedload(models.Proposta.cliente)
        )
        .order_by(models.Proposta.id.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_propostas_por_vendedor(db: AsyncSession, vendedor_id: int) -> List[models.Proposta]:
    '''Lista propostas de um vendedor específico'''
    query = (
        select(models.Proposta)
        .where(models.Proposta.vendedor_id == vendedor_id) # O filtro de permissão
        .options(
            joinedload(models.Proposta.vendedor_responsavel),
            joinedload(models.Proposta.cliente)
        )
        .order_by(models.Proposta.id.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()