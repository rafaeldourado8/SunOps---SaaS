from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from uuid import UUID

from shared.domain.entity import Entity
from shared.domain.value_objects import Money


class StatusProposta(Enum):
    RASCUNHO = "RASCUNHO"
    AGUARDANDO_APROVACAO = "AGUARDANDO"
    APROVADA = "APROVADA"
    ENVIADA = "ENVIADA"
    ACEITA = "ACEITA"
    RECUSADA = "RECUSADA"


@dataclass
class ItemProposta:
    nome: str
    quantidade: int
    preco_unitario: Money
    custo_unitario: Money
    
    def calcular_total_preco(self) -> Money:
        return self.preco_unitario * self.quantidade
    
    def calcular_total_custo(self) -> Money:
        return self.custo_unitario * self.quantidade


@dataclass
class Desconto:
    valor: Money
    motivo: str
    solicitante_id: UUID
    aprovador_id: Optional[UUID] = None
    feedback: Optional[str] = None


@dataclass
class Proposta(Entity):
    vendedor_id: UUID = None
    cliente_id: UUID = None
    potencia_sistema_kwp: float = 0.0
    itens: List[ItemProposta] = field(default_factory=list)
    status: StatusProposta = StatusProposta.RASCUNHO
    desconto: Optional[Desconto] = None
    payback_anos: Optional[float] = None
    
    def adicionar_item(self, item: ItemProposta):
        self.itens.append(item)
    
    def calcular_valor_total(self) -> Money:
        total = sum(item.calcular_total_preco().value for item in self.itens)
        if self.desconto:
            total -= self.desconto.valor.value
        return Money(max(0, total))
    
    def calcular_custo_total(self) -> Money:
        total = sum(item.calcular_total_custo().value for item in self.itens)
        return Money(total)
    
    def solicitar_desconto(self, valor: Money, motivo: str, solicitante_id: UUID):
        if self.status != StatusProposta.RASCUNHO:
            raise ValueError("Desconto só pode ser solicitado em propostas rascunho")
        
        self.desconto = Desconto(valor=valor, motivo=motivo, solicitante_id=solicitante_id)
        self.status = StatusProposta.AGUARDANDO_APROVACAO
    
    def aprovar_desconto(self, aprovador_id: UUID, feedback: Optional[str] = None):
        if not self.desconto:
            raise ValueError("Não há desconto para aprovar")
        
        self.desconto.aprovador_id = aprovador_id
        self.desconto.feedback = feedback
        self.status = StatusProposta.APROVADA
    
    def enviar(self):
        if self.status not in [StatusProposta.APROVADA, StatusProposta.RASCUNHO]:
            raise ValueError("Proposta deve estar aprovada ou em rascunho")
        self.status = StatusProposta.ENVIADA