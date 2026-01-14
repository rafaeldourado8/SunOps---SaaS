"""Value Objects para Unidade Consumidora."""
from dataclasses import dataclass
from typing import List
from decimal import Decimal


@dataclass(frozen=True)
class TipoLigacao:
    """Tipo de ligação elétrica."""
    MONOFASICA = "MONOFASICA"
    BIFASICA = "BIFASICA"
    TRIFASICA = "TRIFASICA"
    
    valor: str
    
    def __post_init__(self):
        if self.valor not in [self.MONOFASICA, self.BIFASICA, self.TRIFASICA]:
            raise ValueError("Tipo de ligação inválido")
    
    @property
    def custo_disponibilidade(self) -> int:
        """Retorna custo de disponibilidade em kWh."""
        return {
            self.MONOFASICA: 30,
            self.BIFASICA: 50,
            self.TRIFASICA: 100
        }[self.valor]


@dataclass(frozen=True)
class Tensao:
    """Tensão da rede."""
    valor: int
    
    def __post_init__(self):
        if self.valor not in [127, 220, 380]:
            raise ValueError("Tensão deve ser 127V, 220V ou 380V")


@dataclass(frozen=True)
class ClasseTarifaria:
    """Classe tarifária ANEEL."""
    valor: str
    
    def __post_init__(self):
        validos = ["B1", "B2", "B3", "A4"]
        if self.valor not in validos:
            raise ValueError(f"Classe deve ser uma de: {validos}")


@dataclass(frozen=True)
class Tarifa:
    """Tarifa de energia (TE + TUSD)."""
    te: Decimal
    tusd: Decimal
    
    def __post_init__(self):
        if self.te <= 0 or self.tusd <= 0:
            raise ValueError("Tarifas devem ser positivas")
    
    @property
    def total(self) -> Decimal:
        """Tarifa total por kWh."""
        return self.te + self.tusd


@dataclass(frozen=True)
class Localizacao:
    """Localização geográfica."""
    latitude: float
    longitude: float
    cidade: str
    
    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude inválida")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude inválida")


@dataclass(frozen=True)
class HistoricoConsumo:
    """Histórico de consumo mensal."""
    consumos_kwh: List[int]
    
    def __post_init__(self):
        if len(self.consumos_kwh) < 1 or len(self.consumos_kwh) > 12:
            raise ValueError("Histórico deve ter 1 a 12 meses")
        if any(c <= 0 for c in self.consumos_kwh):
            raise ValueError("Consumos devem ser positivos")
    
    @property
    def media_mensal(self) -> Decimal:
        """Consumo médio mensal."""
        return Decimal(sum(self.consumos_kwh)) / Decimal(len(self.consumos_kwh))
