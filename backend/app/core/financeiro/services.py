from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date
from typing import List, Optional

from . import models, schema
from app.core.sales.propostas.models import Proposta # Para calcular comissão

async def get_configuracoes(db: AsyncSession) -> models.ConfiguracaoFinanceira:
    '''Busca as configurações financeiras (ou cria se não existirem)'''
    query = select(models.ConfiguracaoFinanceira).where(models.ConfiguracaoFinanceira.id == 1)
    result = await db.execute(query)
    config = result.scalars().first()
    
    # Se for o primeiro acesso, cria a linha de configuração padrão
    if not config:
        config = models.ConfiguracaoFinanceira()
        db.add(config)
        await db.commit()
        await db.refresh(config)
    return config

async def update_configuracoes(
    db: AsyncSession, 
    config_update: schema.UpdateConfiguracaoFinanceira
) -> models.ConfiguracaoFinanceira:
    '''Atualiza as configurações financeiras'''
    config = await get_configuracoes(db)
    
    config.margem_lucro_padrao = config_update.margem_lucro_padrao
    config.percentual_comissao_padrao = config_update.percentual_comissao_padrao
    
    await db.commit()
    await db.refresh(config)
    return config

async def get_transacoes_vencidas_pendentes(db: AsyncSession) -> List[models.Transacao]:
    '''Busca transações para o alerta do dashboard'''
    query = (
        select(models.Transacao)
        .where(
            models.Transacao.status == models.StatusTransacao.PENDENTE,
            models.Transacao.data_vencimento < date.today()
        )
    )
    result = await db.execute(query)
    transacoes = result.scalars().all()
    
    # Opcional: Atualiza o status para "ATRASADA"
    for t in transacoes:
        t.status = models.StatusTransacao.ATRASADA
    if transacoes:
        await db.commit()
        
    return transacoes

async def get_all_transacoes(db: AsyncSession) -> List[models.Transacao]:
    '''Lista todas as transações'''
    query = select(models.Transacao).order_by(models.Transacao.data_vencimento.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def get_transacao_by_id(db: AsyncSession, transacao_id: int) -> Optional[models.Transacao]:
    query = select(models.Transacao).where(models.Transacao.id == transacao_id)
    result = await db.execute(query)
    return result.scalars().first()

async def marcar_transacao_paga(db: AsyncSession, transacao: models.Transacao) -> models.Transacao:
    '''Marca uma transação como paga'''
    transacao.status = models.StatusTransacao.PAGA
    transacao.data_pagamento = datetime.utcnow()
    await db.commit()
    await db.refresh(transacao)
    return transacao

# --- Lógica de Negócio (chamada por outros módulos) ---

async def criar_transacao_entrada_projeto(db: AsyncSession, proposta_ganha: Proposta):
    '''Chamado pelo módulo 'sales' quando uma proposta é 'GANHA' '''
    
    # Regra de negócio: A entrada é 30% do valor total?
    valor_entrada = proposta_ganha.valor_total * Decimal(0.30)
    
    nova_transacao = models.Transacao(
        descricao=f"Pagamento da entrada do Projeto {proposta_ganha.cliente.nome_razao_social}",
        valor=valor_entrada,
        tipo=models.TipoTransacao.ENTRADA_PROJETO,
        status=models.StatusTransacao.PENDENTE,
        data_vencimento=date.today() + timedelta(days=5), # Vence em 5 dias
        projeto_id=proposta_ganha.projeto.id, # Assumindo que o projeto é criado junto
    )
    db.add(nova_transacao)
    # O commit será feito pelo serviço chamador