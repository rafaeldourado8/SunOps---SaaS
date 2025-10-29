from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional
from datetime import date
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