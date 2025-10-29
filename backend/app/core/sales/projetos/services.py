from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List, Optional

from . import models, schema

async def create_projeto(db: AsyncSession, projeto: schema.ProjetoCreate) -> models.Projeto:
    '''Cria um novo projeto no banco'''
    db_projeto = models.Projeto(**projeto.model_dump())
    db.add(db_projeto)
    await db.commit()
    await db.refresh(db_projeto)
    return await get_projeto_by_id(db, db_projeto.id) # Retorna com dados aninhados

async def get_projeto_by_id(db: AsyncSession, projeto_id: int) -> Optional[models.Projeto]:
    '''Busca um projeto com dados do cliente e responsável'''
    query = (
        select(models.Projeto)
        .where(models.Projeto.id == projeto_id)
        .options(
            joinedload(models.Projeto.gestor_responsavel), # Carrega o User
            joinedload(models.Projeto.cliente)           # Carrega o Cliente
        )
    )
    result = await db.execute(query)
    return result.scalars().first()

async def get_all_projetos(db: AsyncSession) -> List[models.Projeto]:
    '''Lista todos os projetos (para Gestores)'''
    query = (
        select(models.Projeto)
        .options(
            joinedload(models.Projeto.gestor_responsavel),
            joinedload(models.Projeto.cliente)
        )
        .order_by(models.Projeto.id.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_projetos_por_responsavel(db: AsyncSession, responsavel_id: int) -> List[models.Projeto]:
    '''Lista projetos de um responsável específico (para Vendedores)'''
    query = (
        select(models.Projeto)
        .where(models.Projeto.responsavel_id == responsavel_id) # O filtro de permissão
        .options(
            joinedload(models.Projeto.gestor_responsavel),
            joinedload(models.Projeto.cliente)
        )
        .order_by(models.Projeto.id.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()