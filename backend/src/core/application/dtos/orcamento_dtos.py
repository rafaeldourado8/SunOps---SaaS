from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class CriarKitDTO:
    nome: str
    is_template: bool = False

@dataclass
class AdicionarItemDTO:
    kit_id: str
    categoria: str
    nome: str
    marca: str
    potencia_watts: Optional[int]
    preco: Decimal
    quantidade: int
    descricao: str

@dataclass
class CriarOrcamentoDTO:
    kit_id: str
    cliente_nome: str
    cliente_contato: str
    validade_dias: int = 3

@dataclass
class AprovarOrcamentoDTO:
    orcamento_id: str
    aprovador: str
