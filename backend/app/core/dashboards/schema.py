from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import List, Optional
from app.core.sales.propostas.schema import ShowProposta
from app.core.sales.projetos.schema import ShowProjeto
from app.core.financeiro.schema import ShowTransacao # Para os alertas

# --- Schemas Genéricos ---

class KPI(BaseModel):
    '''Um único "Key Performance Indicator" (Card)'''
    titulo: str
    valor: str # Usamos string para já formatar (ex: "R$ 847.300" ou "18")
    percentual_crescimento: Optional[float] = None # Ex: +12.1%

class FunilEtapa(BaseModel):
    '''Uma etapa do "Funil de Propostas"'''
    status: str # "Novas", "Em Negociação", etc.
    contagem: int
    valor_total: Decimal

class Alerta(BaseModel):
    '''Um item no card "Alertas Importantes"'''
    tipo: str # "financeiro", "proposta"
    titulo: str
    descricao: str
    link_id: int # ID do projeto ou proposta para criar o link

# --- Schema Dashboard GESTOR ---

class DashboardGestor(BaseModel):
    kpis: List[KPI]
    funil_propostas: List[FunilEtapa]
    alertas: List[Alerta]
    projetos_recentes: List[ShowProjeto] # Reutiliza o schema de Projeto

    model_config = ConfigDict(from_attributes=True)

# --- Schema Dashboard VENDEDOR ---

class Pendencia(BaseModel):
    '''Um item no card "Minhas Pendências"'''
    tipo: str # "follow_up", "documentacao", "vencimento"
    titulo: str
    descricao: str
    link_id: int # ID da proposta

class DashboardVendedor(BaseModel):
    saudacao: str # "Bom dia, Rafael!"
    kpis: List[KPI]
    meta_percentual: float # Ex: 67%
    ranking: int # Ex: 2º
    pendencias: List[Pendencia]
    meus_projetos: List[ShowProjeto] # Reutiliza o schema de Projeto

    model_config = ConfigDict(from_attributes=True)