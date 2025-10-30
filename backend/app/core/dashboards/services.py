from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, extract
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Any

from app.core.users.models import User, UserRole
from app.core.sales.propostas.models import Proposta, PropostaStatus
from app.core.sales.projetos.models import Projeto, ProjetoStatus
from app.core.clientes.models import Cliente
from app.core.financeiro.models import Transacao, StatusTransacao
from app.core.sales.projetos import services as projeto_services 
from . import schema

# --- Funções de Cálculo GESTOR ---

async def build_gestor_dashboard(db: AsyncSession) -> schema.DashboardGestor:
    '''Calcula todos os dados para o Dashboard do Gestor'''
    
    # 1. KPIs Principais e Funil (em uma única query)
    kpis, funil = await _get_gestor_kpis_e_funil(db)
    
    # 2. Novos Clientes
    kpis.append(await _get_kpi_novos_clientes(db))
    
    # 3. Projetos Ativos
    kpis.append(await _get_kpi_projetos_ativos(db))
    
    # 4. Alertas Importantes
    alertas = await _get_alertas_gestor(db)
    
    # 5. Projetos Recentes (Reutiliza o service de Projetos)
    projetos_recentes = await projeto_services.get_all_projetos(db) # Pega todos
    
    return schema.DashboardGestor(
        kpis=kpis,
        funil_propostas=funil,
        alertas=alertas,
        projetos_recentes=projetos_recentes[:5] # Limita aos 5 mais recentes
    )

async def _get_gestor_kpis_e_funil(db: AsyncSession):
    '''Calcula KPIs de Propostas e o Funil de Vendas'''
    mes_atual = datetime.utcnow().month
    ano_atual = datetime.utcnow().year

    # Query complexa que agrupa por status (CORRIGIDO)
    query = (
        select(
            Proposta.status,
            func.count(Proposta.id).label("contagem"),
            func.sum(Proposta.valor_total).label("valor_total")
        )
        .group_by(Proposta.status)
    )
    result = await db.execute(query)
    
    # Processa os resultados
    kpis: List[schema.KPI] = []
    funil: List[schema.FunilEtapa] = []
    
    total_em_negociacao = Decimal(0)
    ganho_no_mes = Decimal(0)

    for row in result.all():
        # Adiciona ao funil
        funil.append(schema.FunilEtapa(
            status=row.status.value,
            contagem=row.contagem,
            valor_total=row.valor_total
        ))
        
        # Lógica de KPI
        if row.status == PropostaStatus.EM_NEGOCIACAO:
            total_em_negociacao += row.valor_total
            
        if row.status == PropostaStatus.GANHA:
            # Para "Ganhos no Mês", precisamos de uma query mais específica (ou filtrar aqui)
            # Por simplicidade, faremos outra query
            pass 

    # Query específica para "Ganhos no Mês"
    query_ganho_mes = (
        select(func.sum(Proposta.valor_total))
        .where(
            Proposta.status == PropostaStatus.GANHA,
            extract('month', Proposta.data_atualizacao) == mes_atual, # Assumindo data_atualizacao
            extract('year', Proposta.data_atualizacao) == ano_atual
        )
    )
    ganho_no_mes = (await db.execute(query_ganho_mes)).scalar_one_or_none() or Decimal(0)

    # Monta os KPIs
    kpis.append(schema.KPI(
        titulo="Valor em Negociação",
        valor=f"R$ {total_em_negociacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ))
    kpis.append(schema.KPI(
        titulo="Propostas Ganhas (Mês)",
        valor=f"R$ {ganho_no_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ))
    
    return kpis, funil

async def _get_kpi_novos_clientes(db: AsyncSession) -> schema.KPI:
    '''Calcula o KPI de "Novos Clientes" no mês'''
    mes_atual = datetime.utcnow().month
    ano_atual = datetime.utcnow().year
    
    query = (
        select(func.count(Cliente.id))
        .where(
            extract('month', Cliente.data_criacao) == mes_atual, # Assumindo data_criacao
            extract('year', Cliente.data_criacao) == ano_atual
        )
    )
    contagem = (await db.execute(query)).scalar_one()
    return schema.KPI(titulo="Novos Clientes", valor=str(contagem))

async def _get_kpi_projetos_ativos(db: AsyncSession) -> schema.KPI:
    '''Calcula o KPI de "Projetos Ativos"'''
    query = (
        select(func.count(Projeto.id))
        .where(Projeto.status.notin_([ProjetoStatus.INSTALADO, ProjetoStatus.CANCELADO]))
    )
    contagem = (await db.execute(query)).scalar_one()
    return schema.KPI(titulo="Projetos Ativos", valor=str(contagem))

async def _get_alertas_gestor(db: AsyncSession) -> List[schema.Alerta]:
    '''Busca alertas financeiros e de propostas'''
    alertas = []
    
    # 1. Alerta de Pagamento Atrasado (do módulo financeiro)
    query_fin = (
        select(Transacao)
        .where(Transacao.status.in_([StatusTransacao.ATRASADA, StatusTransacao.PENDENTE]))
        .where(Transacao.data_vencimento < datetime.utcnow().date())
    )
    transacoes_atrasadas = (await db.execute(query_fin)).scalars().all()
    
    for t in transacoes_atrasadas:
        alertas.append(schema.Alerta(
            tipo="financeiro",
            titulo="Pagamento Atrasado",
            descricao=t.descricao,
            link_id=t.projeto_id or 0
        ))
        
    # 2. Alerta de Propostas Vencendo (Ex: 3 propostas para revisar)
    # (Lógica similar, buscando propostas)
    
    return alertas

# --- Funções de Cálculo VENDEDOR ---

async def build_vendedor_dashboard(db: AsyncSession, user: User) -> schema.DashboardVendedor:
    '''Calcula todos os dados para o Dashboard do Vendedor'''
    
    # 1. KPIs (filtrados pelo user.id)
    kpis = await _get_vendedor_kpis(db, user.id)
    
    # 2. Meta e Ranking (simplificado)
    meta_percentual = 67.0 # Você buscaria isso de uma tabela de Metas
    ranking = 2 # Você calcularia isso comparando vendedores
    
    # 3. Pendências
    pendencias = await _get_pendencias_vendedor(db, user.id)
    
    # 4. Meus Projetos (Reutiliza o service de Projetos)
    meus_projetos = await projeto_services.get_projetos_por_responsavel(db, user.id)
    
    return schema.DashboardVendedor(
        saudacao=f"Bom dia, {user.name.split(' ')[0]}!", # Pega o primeiro nome
        kpis=kpis,
        meta_percentual=meta_percentual,
        ranking=ranking,
        pendencias=pendencias,
        meus_projetos=meus_projetos
    )

async def _get_vendedor_kpis(db: AsyncSession, vendedor_id: int) -> List[schema.KPI]:
    '''Calcula os KPIs filtrados para um vendedor'''
    mes_atual = datetime.utcnow().month
    ano_atual = datetime.utcnow().year

    # Query base filtrada pelo ID do vendedor
    query_base = select(Proposta).where(Proposta.vendedor_id == vendedor_id)
    
    # 1. KPI "Meu ideal em Negociação"
    query_neg = (
        select(func.sum(Proposta.valor_total))
        .where(Proposta.vendedor_id == vendedor_id)
        .where(Proposta.status == PropostaStatus.EM_NEGOCIACAO)
    )
    total_em_negociacao = (await db.execute(query_neg)).scalar_one_or_none() or Decimal(0)
    
    # 2. KPI "Minhas Vendas (Mês)"
    query_ganho_mes = (
        select(func.sum(Proposta.valor_total))
        .where(Proposta.vendedor_id == vendedor_id)
        .where(Proposta.status == PropostaStatus.GANHA)
        .where(extract('month', Proposta.data_atualizacao) == mes_atual)
        .where(extract('year', Proposta.data_atualizacao) == ano_atual)
    )
    ganho_no_mes = (await db.execute(query_ganho_mes)).scalar_one_or_none() or Decimal(0)

    # Monta os KPIs
    kpis = []
    kpis.append(schema.KPI(
        titulo="Meu ideal em Negociação",
        valor=f"R$ {total_em_negociacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ))
    kpis.append(schema.KPI(
        titulo="Minhas Vendas (Mês)",
        valor=f"R$ {ganho_no_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ))
    
    return kpis

async def _get_pendencias_vendedor(db: AsyncSession, vendedor_id: int) -> List[schema.Pendencia]:
    '''Busca pendências (Propostas Vencendo, Follow-up)'''
    pendencias = []
    
    # 1. Lógica de "Proposta Vencendo"
    query_vencendo = (
        select(Proposta)
        .where(Proposta.vendedor_id == vendedor_id)
        .where(Proposta.status.in_([PropostaStatus.NOVA, PropostaStatus.ENVIADA]))
        .where(Proposta.data_vencimento < (datetime.utcnow().date() + timedelta(days=3))) # Vence nos prox 3 dias
    )
    propostas_vencendo = (await db.execute(query_vencendo)).scalars().all()
    
    for p in propostas_vencendo:
        pendencias.append(schema.Pendencia(
            tipo="vencimento",
            titulo="Proposta Vencendo",
            descricao=f"Proposta para {p.cliente.nome_razao_social} vence em X dias.",
            link_id=p.id
        ))
        
    # 2. Lógica de "Follow-up" (poderia vir de um campo 'proxima_acao_data')
    
    return pendencias