from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.users.models import User, UserRole
from app.core.auth.dependencies import get_current_user # A dependência de login
from . import services, schema, models

router = APIRouter(tags=['Propostas'], prefix='/propostas')

@router.post(
    '/', 
    response_model=schema.ShowProposta, 
    status_code=status.HTTP_201_CREATED
)
async def create_proposta(
    proposta: schema.PropostaCreate,
    db: AsyncSession = Depends(get_db),
    # Qualquer usuário logado (Gestor ou Vendedor) pode criar
    current_user: User = Depends(get_current_user)
):
    '''Cria uma nova proposta comercial'''
    # A proposta é criada em nome do usuário logado
    return await services.create_proposta(db, proposta, current_user.id)


@router.get('/', response_model=List[schema.ShowProposta])
async def get_propostas_lista(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
    Lista as propostas.
    - Gestor: Vê todas as propostas.
    - Vendedor: Vê apenas as suas propostas.
    '''
    
    # AQUI ESTÁ A LÓGICA DE PERMISSÃO (RBAC)
    if current_user.role == UserRole.GESTOR:
        return await services.get_all_propostas(db)
    else:
        # Vendedores e outros veem apenas os seus
        return await services.get_propostas_por_vendedor(db, current_user.id)


@router.get('/{proposta_id}', response_model=schema.ShowProposta)
async def get_proposta_detalhe(
    proposta_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Busca uma proposta específica pelo ID'''
    proposta = await services.get_proposta_by_id(db, proposta_id)
    
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    # PERMISSÃO: Vendedor só pode ver a sua própria proposta
    if (
        current_user.role == UserRole.VENDEDOR and 
        proposta.vendedor_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    return proposta