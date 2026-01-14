"""
Entity Inversor
"""
from dataclasses import dataclass
from decimal import Decimal
from contexts.catalogo.domain.entities.produto import Produto


@dataclass
class Inversor(Produto):
    """Entity Inversor"""
    
    potencia: Decimal = Decimal("0")  # kW
    tipo: str = "STRING"  # STRING, MICROINVERSOR
    fases: int = 1  # 1 ou 3
    
    def __post_init__(self):
        super().__post_init__()
        self.validate_inversor()
    
    def validate_inversor(self):
        if self.potencia <= 0:
            raise ValueError("Potência deve ser maior que zero")
        
        if self.tipo not in ["STRING", "MICROINVERSOR"]:
            raise ValueError("Tipo inválido")
        
        if self.fases not in [1, 3]:
            raise ValueError("Fases deve ser 1 ou 3")
