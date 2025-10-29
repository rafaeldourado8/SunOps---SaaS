from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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

@router.get(
    '/configuracoes', 
    response_model=schema.ShowConfiguracaoFinanceira,
    summary="Busca as configurações financeiras"
)
async def get_configuracoes(
    db: AsyncSession = Depends(get_db)
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