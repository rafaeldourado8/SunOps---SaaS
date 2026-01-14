"""Entities para chat WebSocket entre admin e vendedor."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class StatusMensagem(Enum):
    ENVIADA = "ENVIADA"
    ENTREGUE = "ENTREGUE"
    LIDA = "LIDA"


class TipoRemetente(Enum):
    ADMIN = "ADMIN"
    VENDEDOR = "VENDEDOR"
    IA = "IA"


class StatusConversa(Enum):
    ABERTA = "ABERTA"
    EM_ATENDIMENTO = "EM_ATENDIMENTO"
    RESOLVIDA = "RESOLVIDA"
    FECHADA = "FECHADA"


@dataclass
class Mensagem:
    id: str
    conversa_id: str
    remetente_id: str
    tipo_remetente: TipoRemetente
    conteudo: str
    timestamp: datetime
    status: StatusMensagem = StatusMensagem.ENVIADA
    metadata: Optional[dict] = None


@dataclass
class Conversa:
    id: str
    vendedor_id: str
    admin_id: Optional[str] = None
    assunto: str = "Solicitação de orçamento"
    status: StatusConversa = StatusConversa.ABERTA
    mensagens: List[Mensagem] = field(default_factory=list)
    criada_em: datetime = field(default_factory=datetime.now)
    atualizada_em: datetime = field(default_factory=datetime.now)
    
    def adicionar_mensagem(self, mensagem: Mensagem):
        self.mensagens.append(mensagem)
        self.atualizada_em = datetime.now()
    
    def atribuir_admin(self, admin_id: str):
        self.admin_id = admin_id
        self.status = StatusConversa.EM_ATENDIMENTO
        self.atualizada_em = datetime.now()
    
    def resolver(self):
        self.status = StatusConversa.RESOLVIDA
        self.atualizada_em = datetime.now()
    
    @property
    def mensagens_nao_lidas(self) -> int:
        return sum(1 for m in self.mensagens if m.status != StatusMensagem.LIDA)
