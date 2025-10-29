from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.users.models import User, UserRole
# Importa as dependências de permissão
from app.core.auth.dependencies import get_current_user, get_current_gestor
from . import services, schema, models

router = APIRouter(tags=['Projetos'], prefix='/projetos')

@router.post(
    '/', 
    response_model=schema.ShowProjeto, 
    status_code=status.HTTP_201_CREATED
)
async def create_projeto(
    projeto: schema.ProjetoCreate,
    db: AsyncSession = Depends(get_db),
    # Permissão: Apenas Gestores podem criar projetos
    gestor: User = Depends(get_current_gestor)
):
    '''Cria um novo projeto no sistema'''
    return await services.create_projeto(db, projeto)


@router.get('/', response_model=List[schema.ShowProjeto])
async def get_projetos_lista(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
    Lista os projetos.
    - Gestor: Vê todos os projetos.
    - Vendedor: Vê apenas os projetos onde é responsável.
    '''
    
    # AQUI ESTÁ A LÓGICA DE PERMISSÃO (RBAC)
    if current_user.role == UserRole.GESTOR:
        return await services.get_all_projetos(db)
    else:
        # Vendedores e outros veem apenas os seus
        return await services.get_projetos_por_responsavel(db, current_user.id)


@router.get('/{projeto_id}', response_model=schema.ShowProjeto)
async def get_projeto_detalhe(
    projeto_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Busca um projeto específico pelo ID'''
    projeto = await services.get_projeto_by_id(db, projeto_id)
    
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    # PERMISSÃO: Vendedor só pode ver o seu próprio projeto
    if (
        current_user.role == UserRole.VENDEDOR and 
        projeto.responsavel_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    return projeto