"""
Service: Calculadora de Geração
"""
from decimal import Decimal


class CalculadoraGeracao:
    """Calcula geração de energia (kWh/mês)"""
    
    @staticmethod
    def calcular(potencia_kwp: Decimal, hsp: Decimal = Decimal("5.0")) -> Decimal:
        """
        Calcula geração mensal
        
        Args:
            potencia_kwp: Potência do sistema em kWp
            hsp: Horas de Sol Pleno (média Brasil: 5h)
        
        Returns:
            Geração em kWh/mês
        
        Fórmula: Potência (kWp) × HSP × 30 dias × 0.8 (perdas)
        """
        if potencia_kwp <= 0:
            raise ValueError("Potência deve ser maior que zero")
        
        if hsp <= 0:
            raise ValueError("HSP deve ser maior que zero")
        
        geracao_mensal = potencia_kwp * hsp * Decimal("30") * Decimal("0.8")
        return geracao_mensal.quantize(Decimal("0.01"))
