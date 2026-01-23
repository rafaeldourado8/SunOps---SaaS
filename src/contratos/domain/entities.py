from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from shared.domain.entity import Entity
from shared.domain.value_objects import Money


class StatusContrato(Enum):
    RASCUNHO = "RASCUNHO"
    ATIVO = "ATIVO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"


@dataclass
class Contrato(Entity):
    proposta_id: UUID = None
    cliente_id: UUID = None
    vendedor_id: UUID = None
    valor_total: Money = None
    data_assinatura: date = None
    status: StatusContrato = StatusContrato.RASCUNHO
    data_conclusao: Optional[date] = None
    observacoes: str = ""
    
    def ativar(self):
        if self.status != StatusContrato.RASCUNHO:
            raise ValueError("Apenas contratos em rascunho podem ser ativados")
        self.status = StatusContrato.ATIVO
    
    def concluir(self, data_conclusao: date):
        if self.status != StatusContrato.ATIVO:
            raise ValueError("Apenas contratos ativos podem ser concluídos")
        self.data_conclusao = data_conclusao
        self.status = StatusContrato.CONCLUIDO
    
    def cancelar(self):
        if self.status == StatusContrato.CONCLUIDO:
            raise ValueError("Contratos concluídos não podem ser cancelados")
        self.status = StatusContrato.CANCELADO