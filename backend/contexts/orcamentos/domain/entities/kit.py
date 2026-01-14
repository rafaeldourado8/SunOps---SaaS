"""
Entity Kit
"""
from dataclasses import dataclass, field
from typing import List
from decimal import Decimal


@dataclass
class ItemKit:
    """Item do Kit"""
    produto_id: int
    produto_nome: str
    quantidade: int
    preco_unitario: Decimal
    
    @property
    def preco_total(self) -> Decimal:
        return self.preco_unitario * self.quantidade


@dataclass
class Kit:
    """Entity Kit"""
    nome: str
    itens: List[ItemKit] = field(default_factory=list)
    
    def adicionar_item(self, item: ItemKit):
        self.itens.append(item)
    
    def remover_item(self, produto_id: int):
        self.itens = [i for i in self.itens if i.produto_id != produto_id]
    
    @property
    def preco_total(self) -> Decimal:
        return sum(item.preco_total for item in self.itens)
    
    @property
    def quantidade_itens(self) -> int:
        return len(self.itens)
