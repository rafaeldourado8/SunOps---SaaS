from dataclasses import dataclass
from datetime import datetime
from typing import Any
from .value_objects import OrcamentoId, KitId

@dataclass(frozen=True)
class DomainEvent:
    """Base para todos os eventos de domínio"""
    ocorrido_em: datetime
    
    def __post_init__(self):
        object.__setattr__(self, 'ocorrido_em', datetime.now())

@dataclass(frozen=True)
class KitCriado(DomainEvent):
    kit_id: KitId
    nome: str
    is_template: bool

@dataclass(frozen=True)
class ItemAdicionado(DomainEvent):
    kit_id: KitId
    item_id: str
    categoria: str

@dataclass(frozen=True)
class ItemRemovido(DomainEvent):
    kit_id: KitId
    item_id: str

@dataclass(frozen=True)
class OrcamentoCriado(DomainEvent):
    orcamento_id: OrcamentoId
    kit_id: KitId
    cliente_nome: str

@dataclass(frozen=True)
class OrcamentoAprovado(DomainEvent):
    orcamento_id: OrcamentoId
    aprovado_por: str

@dataclass(frozen=True)
class OrcamentoEnviado(DomainEvent):
    orcamento_id: OrcamentoId
    cliente_contato: str

@dataclass(frozen=True)
class OrcamentoExpirado(DomainEvent):
    orcamento_id: OrcamentoId
    data_expiracao: datetime
