"""
Entity Fornecedor (Domain Layer)
"""
from dataclasses import dataclass
from typing import Optional
from shared.domain.value_objects.cnpj import CNPJ
from shared.domain.value_objects.email import Email
from shared.domain.value_objects.telefone import Telefone


@dataclass
class Fornecedor:
    """Entity Fornecedor seguindo DDD"""
    
    nome: str
    cnpj: CNPJ
    email: Email
    telefone: Telefone
    endereco: Optional[str] = None
    ativo: bool = True
    id: Optional[int] = None
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        """Valida regras de negócio"""
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")
        
        if len(self.nome) > 200:
            raise ValueError("Nome deve ter no máximo 200 caracteres")
    
    def ativar(self):
        """Ativa fornecedor"""
        self.ativo = True
    
    def desativar(self):
        """Desativa fornecedor"""
        self.ativo = False
