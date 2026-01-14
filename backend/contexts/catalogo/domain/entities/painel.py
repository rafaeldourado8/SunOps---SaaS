"""
Entity Painel
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from contexts.catalogo.domain.entities.produto import Produto


@dataclass
class Painel(Produto):
    """Entity Painel Solar"""
    
    potencia: Decimal = Decimal("0")  # Watts
    eficiencia: Decimal = Decimal("0")  # %
    tipo: str = "MONOCRISTALINO"  # MONOCRISTALINO, POLICRISTALINO
    
    def __post_init__(self):
        super().__post_init__()
        self.validate_painel()
    
    def validate_painel(self):
        if self.potencia <= 0:
            raise ValueError("Potência deve ser maior que zero")
        
        if self.eficiencia < 0 or self.eficiencia > 100:
            raise ValueError("Eficiência deve estar entre 0 e 100%")
        
        if self.tipo not in ["MONOCRISTALINO", "POLICRISTALINO"]:
            raise ValueError("Tipo inválido")
