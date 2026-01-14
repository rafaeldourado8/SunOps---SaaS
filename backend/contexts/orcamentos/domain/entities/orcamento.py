"""
Entity Orcamento
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime
from contexts.orcamentos.domain.entities.kit import Kit


@dataclass
class Orcamento:
    """Entity Orçamento"""
    cliente_id: int
    vendedor_id: int
    kit: Kit
    valor_total: Decimal
    status: str = "RASCUNHO"  # RASCUNHO, ENVIADO, APROVADO, REJEITADO
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if self.valor_total < 0:
            raise ValueError("Valor total não pode ser negativo")
        
        if self.status not in ["RASCUNHO", "ENVIADO", "APROVADO", "REJEITADO"]:
            raise ValueError("Status inválido")
    
    def enviar(self):
        self.status = "ENVIADO"
    
    def aprovar(self):
        self.status = "APROVADO"
    
    def rejeitar(self):
        self.status = "REJEITADO"
