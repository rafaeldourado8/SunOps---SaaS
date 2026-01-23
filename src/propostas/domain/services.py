from dataclasses import dataclass

from .entities import Proposta


@dataclass
class CalculadoraPayback:
    
    def calcular(self, proposta: Proposta, economia_mensal: float) -> float:
        if economia_mensal <= 0:
            raise ValueError("Economia mensal deve ser maior que zero")
        
        valor_total = proposta.calcular_valor_total().value
        economia_anual = economia_mensal * 12
        
        return round(valor_total / economia_anual, 1)
