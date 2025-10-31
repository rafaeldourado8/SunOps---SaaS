
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import List, Optional, Any
from .models import PropostaStatus, PropostaItem
from app.core.users.schema import ShowUser
from app.core.clientes.schema import ShowCliente 

# --- Schema para PropostaItem ---
class PropostaItemBase(BaseModel):
    categoria: str = "Custos"
    descricao: str
    quantidade: int = 1
    custo_unitario: Decimal = 0.0
    impostos: Decimal = 0.0
    margem: Decimal = 0.0
    valor_venda: Decimal = 0.0 # Este é o campo "Valores" da sua imagem

class PropostaItemCreate(PropostaItemBase):
    pass

class ShowPropostaItem(PropostaItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Schema para Proposta ---

class PropostaBase(BaseModel):
    # Campos adicionados
    nome: Optional[str] = None
    potencia_kwp: Optional[float] = None
    premissas: Optional[dict[str, Any]] = None
    
    # Campos que já existiam (valor_total será calculado a partir dos itens)
    valor_total: Decimal = 0.0 
    cliente_id: int
    status: PropostaStatus = PropostaStatus.NOVA

class PropostaCreate(PropostaBase):
    # Ao criar uma proposta, esperamos uma lista de itens (opcional)
    itens: List[PropostaItemCreate] = []

class ShowProposta(PropostaBase):
    id: int
    vendedor_responsavel: ShowUser # Objeto aninhado
    cliente: ShowCliente          # Objeto aninhado
    
    # Ao exibir uma proposta, mostramos a lista de itens
    itens: List[ShowPropostaItem] = []

    model_config = ConfigDict(from_attributes=True)

# Schema para atualizar o status (continua o mesmo)
class PropostaUpdateStatus(BaseModel):
    status: PropostaStatus

# --- NOVOS SCHEMAS ADICIONADOS ---

# 1. Schema para receber dados da Etapa 1 (Dimensionamento)
class PropostaUpdateDimensionamento(BaseModel):
    premissas: dict[str, Any]
    potencia_kwp: float
    
    # --- CAMPOS ALTERADOS ---
    nome_kit: Optional[str] = None         # Em vez de kit_id
    nome_distribuidor: Optional[str] = None # Novo campo
    # --- FIM DA ALTERAÇÃO ---
    
    custo_kit: Optional[Decimal] = None # Campo "Custo" da image_f4ffbe.png
    sistema: Optional[str] = None # Campo "Sistema"
    topologia: Optional[str] = None # Campo "Topologia"
    
# 2. Schema para salvar os dados da Etapa 2 (Custos)
class PropostaUpdateItens(BaseModel):
    itens: List[PropostaItemCreate] # Uma lista completa dos itens da tabela
    valor_total: Decimal # O valor total calculado no frontend