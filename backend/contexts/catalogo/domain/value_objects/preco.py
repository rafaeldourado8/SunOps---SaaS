"""
Value Object: Preco com validade
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal


@dataclass(frozen=True)
class Preco:
    """Preço com validade de 3 dias úteis"""
    
    valor: Decimal
    data_cotacao: datetime
    validade_dias: int = 3
    
    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("Preço não pode ser negativo")
    
    @property
    def data_validade(self) -> datetime:
        """Calcula data de validade (3 dias úteis)"""
        dias_adicionados = 0
        data_atual = self.data_cotacao
        
        while dias_adicionados < self.validade_dias:
            data_atual += timedelta(days=1)
            if data_atual.weekday() < 5:
                dias_adicionados += 1
        
        return data_atual
    
    @property
    def esta_valido(self) -> bool:
        """Verifica se preço ainda está válido"""
        return datetime.now() <= self.data_validade
    
    def __str__(self):
        return f"R$ {self.valor:.2f}"
