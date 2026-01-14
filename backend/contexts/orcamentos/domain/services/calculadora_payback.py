"""
Service: Calculadora de Payback
"""
from decimal import Decimal


class CalculadoraPayback:
    """Calcula payback do investimento"""
    
    @staticmethod
    def calcular(investimento: Decimal, economia_mensal: Decimal) -> Decimal:
        """
        Calcula payback em meses
        
        Args:
            investimento: Valor total do investimento
            economia_mensal: Economia mensal em R$
        
        Returns:
            Payback em meses
        """
        if investimento <= 0:
            raise ValueError("Investimento deve ser maior que zero")
        
        if economia_mensal <= 0:
            raise ValueError("Economia mensal deve ser maior que zero")
        
        payback_meses = investimento / economia_mensal
        return payback_meses.quantize(Decimal("0.01"))
