from pydantic import BaseModel, ConfigDict, Field, validator
from decimal import Decimal
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from .models import TipoTransacao, StatusTransacao

# --- Schemas de Configuração ---

class ConfiguracaoFinanceiraBase(BaseModel):
    margem_lucro_padrao: float
    percentual_comissao_padrao: float

class UpdateConfiguracaoFinanceira(ConfiguracaoFinanceiraBase):
    pass

class ShowConfiguracaoFinanceira(ConfiguracaoFinanceiraBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Transação ---

class TransacaoBase(BaseModel):
    descricao: str
    valor: Decimal
    tipo: TipoTransacao
    status: StatusTransacao = StatusTransacao.PENDENTE
    data_vencimento: Optional[date] = None
    projeto_id: Optional[int] = None
    vendedor_id: Optional[int] = None

class TransacaoCreate(TransacaoBase):
    pass

class ShowTransacao(TransacaoBase):
    id: int
    data_criacao: date
    
    # Você pode adicionar ShowProjeto, ShowUser se quiser mostrar os objetos
    # projeto: Optional[ShowProjeto] = None 
    # vendedor: Optional[ShowUser] = None

    model_config = ConfigDict(from_attributes=True)


# --- INÍCIO DO NOVO CÓDIGO DA FEATURE DE PREMISSAS ---

# --- Schemas de Faixa de Premissa ---

class PremissaFaixaBase(BaseModel):
    nome_faixa: str = Field(..., examples=["Micro (≤4kW)"])
    potencia_min: float = Field(..., examples=[0.01])
    potencia_max: float = Field(..., examples=[4.0])
    preco_unitario: Decimal = Field(..., max_digits=10, decimal_places=4, examples=[0.23])
    ordem: int = 0

class PremissaFaixaCreate(PremissaFaixaBase):
    pass

class ShowPremissaFaixa(PremissaFaixaBase):
    id: int
    premissa_id: int
    criada_em: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Região de Premissa ---

class PremissaPorRegiaoBase(BaseModel):
    regiao: str = Field(..., examples=["SP", "RJ", "MG"])
    aliquota_imposto: float = Field(..., examples=[0.16])
    observacoes: Optional[str] = None

class PremissaPorRegiaoCreate(PremissaPorRegiaoBase):
    pass

class ShowPremissaPorRegiao(PremissaPorRegiaoBase):
    id: int
    premissa_id: int
    criada_em: datetime
    
    model_config = ConfigDict(from_attributes=True)


# --- Schemas da Premissa Principal ---

class PremissaBase(BaseModel):
    nome: str = Field(..., examples=["Tabela Q4 2024"])
    descricao: Optional[str] = None
    data_vigencia_inicio: date
    data_vigencia_fim: date
    ativa: bool = True

class PremissaCreate(PremissaBase):
    """Schema para criar uma premissa, incluindo suas faixas e regiões."""
    faixas: List[PremissaFaixaCreate] = []
    regioes: List[PremissaPorRegiaoCreate] = []

    @validator('data_vigencia_fim')
    def validar_datas(cls, data_fim, values):
        if 'data_vigencia_inicio' in values and data_fim < values['data_vigencia_inicio']:
            raise ValueError("A data final da vigência não pode ser anterior à data inicial.")
        return data_fim

class PremissaUpdate(BaseModel):
    """Schema para atualizar apenas os dados da premissa (faixas/regiões são atualizadas em endpoints próprios)."""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    data_vigencia_inicio: Optional[date] = None
    data_vigencia_fim: Optional[date] = None
    ativa: Optional[bool] = None

    model_config = ConfigDict(extra='forbid')


class ShowPremissa(PremissaBase):
    id: int
    empresa_id: int
    criada_em: datetime
    atualizada_em: datetime
    faixas: List[ShowPremissaFaixa] = []
    regioes: List[ShowPremissaPorRegiao] = []

    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Cálculo de Preço ---

class CalculoPrecosRequest(BaseModel):
    potencia_kw: float = Field(..., gt=0, examples=[5.5])
    regiao: str = Field(..., examples=["SP"])
    data: date = Field(default_factory=date.today)
    
    # Opcionais
    premissa_id: Optional[int] = None # Se null, usa a ativa mais recente
    custos_adicionais: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)
    
    # Overrides
    margem_lucro_override: Optional[float] = None # Ex: 0.25 (25%)
    comissao_override: Optional[float] = None # Ex: 0.05 (5%)
    imposto_override: Optional[float] = None # Ex: 0.18 (18%)


class CalculoPrecosResponse(BaseModel):
    # Inputs
    potencia_solicitada_kw: float
    regiao: str
    data_calculo: date
    
    # Premissa
    premissa_usada_id: int
    premissa_usada_nome: str
    
    # Faixa
    faixa_aplicada_nome: str
    preco_unitario_wp: Decimal # R$/Wp
    
    # Cálculo
    preco_base: Decimal # (potencia_kw * 1000) * preco_unitario_wp
    custos_adicionais: Decimal
    subtotal_custos: Decimal # (preco_base + custos_adicionais)
    
    # Margens e Comissões (Valores)
    margem_lucro_percentual: float
    margem_lucro_valor: Decimal
    comissao_percentual: float
    comissao_valor: Decimal
    
    # Imposto
    subtotal_sem_imposto: Decimal # (subtotal_custos + margem + comissao)
    imposto_percentual: float
    imposto_valor: Decimal
    
    # Final
    preco_final: Decimal # (subtotal_sem_imposto + imposto_valor)

    # Detalhes
    detalhes: Dict[str, Any] = Field(description="Valores intermediários e overrides utilizados")

# --- FIM DO NOVO CÓDIGO DA FEATURE DE PREMISSAS ---