from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
from .entities import Kit
from .value_objects import OrcamentoId, Dinheiro
from .events import (
    DomainEvent, OrcamentoCriado, OrcamentoAprovado, 
    OrcamentoEnviado, OrcamentoExpirado
)
from .exceptions import (
    OrcamentoInvalidoException, OrcamentoExpiradoException, StatusInvalidoException
)

class StatusOrcamento(str, Enum):
    RASCUNHO = "rascunho"
    EM_REVISAO = "em_revisao"
    APROVADO = "aprovado"
    ENVIADO = "enviado"
    ACEITO = "aceito"
    RECUSADO = "recusado"
    EXPIRADO = "expirado"

@dataclass
class Orcamento:
    """Aggregate Root: Orçamento"""
    id: OrcamentoId
    kit: Kit
    cliente_nome: str
    cliente_contato: str
    status: StatusOrcamento = StatusOrcamento.RASCUNHO
    validade_dias: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    aprovado_por: Optional[str] = None
    enviado_em: Optional[datetime] = None
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        if not self.cliente_nome:
            raise OrcamentoInvalidoException("Cliente nome obrigatório")
        if not self.cliente_contato:
            raise OrcamentoInvalidoException("Cliente contato obrigatório")
        
        self._adicionar_evento(OrcamentoCriado(
            datetime.now(),
            self.id,
            self.kit.id,
            self.cliente_nome
        ))
    
    def aprovar(self, aprovador: str) -> None:
        """RN: Apenas rascunho ou em revisão podem ser aprovados"""
        if self.status not in [StatusOrcamento.RASCUNHO, StatusOrcamento.EM_REVISAO]:
            raise StatusInvalidoException(f"Não pode aprovar orçamento com status {self.status}")
        
        if self._esta_expirado():
            raise OrcamentoExpiradoException("Orçamento expirado")
        
        self.status = StatusOrcamento.APROVADO
        self.aprovado_por = aprovador
        self.updated_at = datetime.now()
        
        self._adicionar_evento(OrcamentoAprovado(
            datetime.now(),
            self.id,
            aprovador
        ))
    
    def enviar(self) -> None:
        """RN: Apenas aprovados podem ser enviados"""
        if self.status != StatusOrcamento.APROVADO:
            raise StatusInvalidoException("Apenas orçamentos aprovados podem ser enviados")
        
        if self._esta_expirado():
            raise OrcamentoExpiradoException("Orçamento expirado")
        
        self.status = StatusOrcamento.ENVIADO
        self.enviado_em = datetime.now()
        self.updated_at = datetime.now()
        
        self._adicionar_evento(OrcamentoEnviado(
            datetime.now(),
            self.id,
            self.cliente_contato
        ))
    
    def aceitar(self) -> None:
        if self.status != StatusOrcamento.ENVIADO:
            raise StatusInvalidoException("Apenas orçamentos enviados podem ser aceitos")
        self.status = StatusOrcamento.ACEITO
        self.updated_at = datetime.now()
    
    def recusar(self) -> None:
        if self.status != StatusOrcamento.ENVIADO:
            raise StatusInvalidoException("Apenas orçamentos enviados podem ser recusados")
        self.status = StatusOrcamento.RECUSADO
        self.updated_at = datetime.now()
    
    def marcar_como_expirado(self) -> None:
        """RN13: Marca orçamento como expirado após validade"""
        self.status = StatusOrcamento.EXPIRADO
        self.updated_at = datetime.now()
        
        self._adicionar_evento(OrcamentoExpirado(
            datetime.now(),
            self.id,
            self._calcular_data_validade()
        ))
    
    def calcular_total(self) -> Dinheiro:
        return self.kit.calcular_total()
    
    def _calcular_data_validade(self) -> datetime:
        """RN10: Preço válido por 3 dias úteis"""
        return self.created_at + timedelta(days=self.validade_dias)
    
    def _esta_expirado(self) -> bool:
        """RN13: Verifica se orçamento está válido"""
        return datetime.now() >= self._calcular_data_validade()
    
    def _adicionar_evento(self, evento: DomainEvent) -> None:
        self._events.append(evento)
    
    def obter_eventos(self) -> List[DomainEvent]:
        return self._events.copy()
    
    def limpar_eventos(self) -> None:
        self._events.clear()
