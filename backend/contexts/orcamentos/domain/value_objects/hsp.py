"""HSP - Horas de Sol Pleno."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class HSP:
    """Horas de Sol Pleno médio diário."""
    valor: Decimal
    fonte: str  # CRESESB, PVGIS, API
    inclinacao: int = 15
    azimute: int = 0
    
    def __post_init__(self):
        if self.valor <= 0 or self.valor > 12:
            raise ValueError("HSP deve estar entre 0 e 12 horas")
        if not (0 <= self.inclinacao <= 90):
            raise ValueError("Inclinação deve estar entre 0° e 90°")
        if not (-180 <= self.azimute <= 180):
            raise ValueError("Azimute deve estar entre -180° e 180°")
