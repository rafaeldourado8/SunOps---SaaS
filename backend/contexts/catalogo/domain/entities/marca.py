"""
Entity Marca (Domain Layer)
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Marca:
    """Entity Marca seguindo DDD"""
    
    nome: str
    ativo: bool = True
    id: Optional[int] = None
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        """Valida regras de negócio"""
        if not self.nome or len(self.nome) < 2:
            raise ValueError("Nome deve ter no mínimo 2 caracteres")
        
        if len(self.nome) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")
    
    def ativar(self):
        self.ativo = True
    
    def desativar(self):
        self.ativo = False
