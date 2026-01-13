from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import NewType
from .exceptions import ValorInvalidoException, QuantidadeInvalidaException

# Value Objects (imutáveis)

ItemId = NewType('ItemId', str)
KitId = NewType('KitId', str)
OrcamentoId = NewType('OrcamentoId', str)

class CategoriaItem(str, Enum):
    PAINEL_SOLAR = "painel_solar"
    INVERSOR = "inversor"
    ESTRUTURA = "estrutura"
    CABO = "cabo"
    CONECTOR = "conector"
    CUSTOMIZADO = "customizado"

@dataclass(frozen=True)
class Dinheiro:
    """Value Object: Representa valor monetário"""
    valor: Decimal
    
    def __post_init__(self):
        if self.valor < 0:
            raise ValorInvalidoException("Valor não pode ser negativo")
    
    def multiplicar(self, quantidade: int) -> 'Dinheiro':
        return Dinheiro(self.valor * quantidade)
    
    def somar(self, outro: 'Dinheiro') -> 'Dinheiro':
        return Dinheiro(self.valor + outro.valor)

@dataclass(frozen=True)
class Quantidade:
    """Value Object: Representa quantidade de itens"""
    valor: int
    
    def __post_init__(self):
        if self.valor <= 0:
            raise QuantidadeInvalidaException("Quantidade deve ser maior que zero")

@dataclass(frozen=True)
class PotenciaWatts:
    """Value Object: Potência em Watts"""
    valor: int
    
    def __post_init__(self):
        if self.valor <= 0:
            raise ValorInvalidoException("Potência deve ser maior que zero")
    
    def para_kwp(self) -> Decimal:
        return Decimal(self.valor) / Decimal(1000)
