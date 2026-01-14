"""
Entity Produto (abstrata)
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Produto:
    """Entity Produto base"""
    
    nome: str
    marca_id: int
    fornecedor_id: int
    preco: Decimal
    ativo: bool = True
    id: Optional[int] = None
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")
        
        if self.preco < 0:
            raise ValueError("Preço não pode ser negativo")
    
    def ativar(self):
        self.ativo = True
    
    def desativar(self):
        self.ativo = False
