from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
# Importações necessárias para o novo código
from datetime import date

from app.db import get_db
from app.core.users.models import User
# Importa a dependência de permissão MÁXIMA
from app.core.auth.dependencies import get_current_gestor
from . import services, schema, models

# Todos os endpoints aqui exigem ser GESTOR
router = APIRouter(
    tags=['Financeiro'], 
    prefix='/financeiro',
    dependencies=[Depends(get_current_gestor)] # Protege o módulo inteiro
)

# --- Endpoints de Configuração e Transações (Existentes) ---

@router.get(
    '/configuracoes', 
    response_model=schema.ShowConfiguracaoFinanceira,
    summary="Busca as configurações financeiras"
)
async def get_configuracoes(
    db: AsyncSession = Depends(get_db),
    # A dependência do router já injeta o usuário, mas não o passa para a função.
    # Para usá-lo, precisamos declará-lo explicitamente.
    # No entanto, a função 'services.get_configuracoes' original não pedia 'user',
    # pois a Config é global (ID 1). Vou manter assim.
):
    '''Busca as configurações financeiras globais (margem, comissão).'''
    return await services.get_configuracoes(db)


@router.put(
    '/configuracoes', 
    response_model=schema.ShowConfiguracaoFinanceira,
    summary="Atualiza as configurações financeiras"
)
async def update_configuracoes(
    config_update: schema.UpdateConfiguracaoFinanceira,
    db: AsyncSession = Depends(get_db)
):
    '''Atualiza as configurações financeiras globais (margem, comissão).'''
    return await services.update_configuracoes(db, config_update)


@router.get(
    '/transacoes', 
    response_model=List[schema.ShowTransacao],
    summary="Lista todas as transações financeiras"
)
async def get_all_transacoes(db: AsyncSession = Depends(get_db)):
    '''Lista todas as transações (entradas, saídas, comissões).'''
    return await services.get_all_transacoes(db)


@router.post(
    '/transacoes/{transacao_id}/marcar-pago', 
    response_model=schema.ShowTransacao,
    summary="Marca uma transação como paga"
)
async def marcar_como_pago(
    transacao_id: int,
    db: AsyncSession = Depends(get_db)
):
    '''Marca uma transação (ex: entrada de projeto) como paga.'''
    transacao = await services.get_transacao_by_id(db, transacao_id)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    if transacao.status == models.StatusTransacao.PAGA:
        raise HTTPException(status_code=400, detail="Transação já está paga")

    return await services.marcar_transacao_paga(db, transacao)


# --- INÍCIO DOS NOVOS ENDPOINTS DA FEATURE DE PREMISSAS ---

# --- Endpoint de Cálculo (O mais importante) ---

@router.post(
    "/calcular-preco",
    response_model=schema.CalculoPrecosResponse,
    summary="Calcula o preço de um sistema usando premissas"
)
async def calcular_preco_sistema(
    calculo_request: schema.CalculoPrecosRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """
    Calcula o preço final de um sistema solar com base nos inputs:
    - **potencia_kw**: Potência do sistema (ex: 5.5)
    - **regiao**: UF (ex: "SP")
    - **data**: Data do cálculo (para vigência)
    - **premissa_id (Opcional)**: Força o uso de uma premissa. Se nulo, busca a mais recente ativa.
    - **Overrides (Opcional)**: Permite sobrepor margem, comissão ou imposto.
    
    Este endpoint *não* salva nenhuma informação, apenas retorna o cálculo.
    """
    return await services.calcular_preco(db, user, calculo_request)


# --- Endpoints de Premissas (CRUD) ---

@router.get(
    "/premissas",
    response_model=List[schema.ShowPremissa],
    summary="Lista todas as premissas de preço"
)
async def listar_premissas(
    ativa: Optional[bool] = Query(None, alias="ativa_apenas", description="Filtrar apenas premissas ativas"),
    data: Optional[date] = Query(None, description="Filtrar premissas vigentes na data (ex: 2025-11-01)"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Lista todas as premissas de preço da empresa, com filtros opcionais."""
    return await services.listar_premissas(db, user, ativa_apenas=ativa, data=data)


@router.post(
    "/premissas",
    response_model=schema.ShowPremissa,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova premissa de preço"
)
async def criar_premissa(
    premissa_create: schema.PremissaCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """
    Cria uma nova premissa de preço.
    
    Inclua as **faixas** e **regiões** no JSON body para criação aninhada.
    """
    return await services.criar_premissa(db, user, premissa_create)


@router.get(
    "/premissas/{premissa_id}",
    response_model=schema.ShowPremissa,
    summary="Busca uma premissa de preço específica"
)
async def get_premissa(
    premissa_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Retorna uma premissa específica com todas as suas faixas e regiões."""
    return await services.get_premissa_by_id(db, premissa_id, user)


@router.put(
    "/premissas/{premissa_id}",
    response_model=schema.ShowPremissa,
    summary="Atualiza os dados de uma premissa"
)
async def update_premissa(
    premissa_id: int,
    premissa_update: schema.PremissaUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """
    Atualiza os dados principais de uma premissa (nome, vigência, ativa).
    
    *Nota: Para atualizar faixas ou regiões, use os endpoints específicos
    (ex: `PUT /premissas/{id}/faixas/{faixa_id}`).*
    """
    return await services.atualizar_premissa(db, premissa_id, user, premissa_update)


@router.delete(
    "/premissas/{premissa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma premissa de preço"
)
async def delete_premissa(
    premissa_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """
    Deleta uma premissa.
    
    *Atenção: Isso deletará em cascata todas as faixas e regiões associadas a ela.*
    """
    await services.deletar_premissa(db, premissa_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Endpoints de Faixas (Sub-recurso de Premissa) ---

@router.post(
    "/premissas/{premissa_id}/faixas",
    response_model=schema.ShowPremissaFaixa,
    status_code=status.HTTP_201_CREATED,
    summary="Adiciona uma faixa de preço a uma premissa"
)
async def adicionar_faixa_premissa(
    premissa_id: int,
    faixa_create: schema.PremissaFaixaCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Adiciona uma nova faixa (ex: 8-12kW) a uma premissa existente."""
    return await services.adicionar_faixa(db, premissa_id, user, faixa_create)


@router.put(
    "/premissas/{premissa_id}/faixas/{faixa_id}",
    response_model=schema.ShowPremissaFaixa,
    summary="Atualiza uma faixa de preço"
)
async def update_faixa_premissa(
    premissa_id: int,
    faixa_id: int,
    faixa_update: schema.PremissaFaixaCreate, # Reutiliza o schema de criação
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Atualiza os dados de uma faixa de preço específica."""
    return await services.atualizar_faixa(db, premissa_id, faixa_id, user, faixa_update)


@router.delete(
    "/premissas/{premissa_id}/faixas/{faixa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove uma faixa de preço"
)
async def delete_faixa_premissa(
    premissa_id: int,
    faixa_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Remove uma faixa de preço de uma premissa."""
    await services.deletar_faixa(db, premissa_id, faixa_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Endpoints de Regiões (Sub-recurso de Premissa) ---

@router.post(
    "/premissas/{premissa_id}/regioes",
    response_model=schema.ShowPremissaPorRegiao,
    status_code=status.HTTP_201_CREATED,
    summary="Adiciona uma configuração de imposto por região"
)
async def adicionar_regiao_premissa(
    premissa_id: int,
    regiao_create: schema.PremissaPorRegiaoCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Adiciona uma alíquota de imposto para uma região (ex: "MG", 0.18)"""
    return await services.adicionar_regiao(db, premissa_id, user, regiao_create)


@router.put(
    "/premissas/{premissa_id}/regioes/{regiao_id}",
    response_model=schema.ShowPremissaPorRegiao,
    summary="Atualiza uma configuração de região"
)
async def update_regiao_premissa(
    premissa_id: int,
    regiao_id: int,
    regiao_update: schema.PremissaPorRegiaoCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Atualiza a alíquota ou observações de uma região."""
    return await services.atualizar_regiao(db, premissa_id, regiao_id, user, regiao_update)


@router.delete(
    "/premissas/{premissa_id}/regioes/{regiao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove uma configuração de região"
)
async def delete_regiao_premissa(
    premissa_id: int,
    regiao_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_gestor)
):
    """Remove uma configuração de imposto por região de uma premissa."""
    await services.deletar_regiao(db, premissa_id, regiao_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- FIM DOS NOVOS ENDPOINTS DA FEATURE DE PREMISSAS ---