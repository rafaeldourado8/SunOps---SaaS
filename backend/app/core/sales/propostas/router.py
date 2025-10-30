# Em app/core/sales/propostas/router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.users.models import User, UserRole
from app.core.auth.dependencies import get_current_user # A dependência de login
from . import services, schema, models

router = APIRouter(tags=['Propostas'], prefix='/propostas')

# ... (Endpoint create_proposta e get_propostas_lista permanecem iguais) ...
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
    
    if current_user.role == UserRole.GESTOR:
        return await services.get_all_propostas(db)
    else:
        return await services.get_propostas_por_vendedor(db, current_user.id)


@router.get('/{proposta_id}', response_model=schema.ShowProposta)
async def get_proposta_detalhe(
    proposta_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Busca uma proposta específica pelo ID (com todos os seus itens)'''
    proposta = await services.get_proposta_by_id(db, proposta_id)
    
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    # PERMISSÃO
    if (
        current_user.role == UserRole.VENDEDOR and 
        proposta.vendedor_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    return proposta

# --- NOVOS ENDPOINTS ADICIONADOS ---

@router.put(
    '/{proposta_id}/dimensionamento', 
    response_model=schema.ShowProposta,
    summary="Salva a Etapa 1 (Dimensionamento) e gera os custos iniciais"
)
async def salvar_dimensionamento(
    proposta_id: int,
    data: schema.PropostaUpdateDimensionamento,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
    Salva os dados da Etapa 1 (kit, premissas) e gera a lista 
    de custos (Etapa 2) com valores padrão.
    '''
    proposta = await services.get_proposta_by_id(db, proposta_id)
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    # PERMISSÃO
    if (
        current_user.role == UserRole.VENDEDOR and 
        proposta.vendedor_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    return await services.save_dimensionamento_e_gerar_custos(db, proposta, data)


@router.put(
    '/{proposta_id}/custos', 
    response_model=schema.ShowProposta,
    summary="Salva a Etapa 2 (Custos e Preço de Venda)"
)
async def salvar_custos(
    proposta_id: int,
    data: schema.PropostaUpdateItens,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
    Recebe a lista de itens de custo editada (Etapa 2) 
    e atualiza a proposta.
    '''
    proposta = await services.get_proposta_by_id(db, proposta_id)
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    # PERMISSÃO
    if (
        current_user.role == UserRole.VENDEDOR and 
        proposta.vendedor_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")
        
    return await services.update_proposta_itens(db, proposta, data)