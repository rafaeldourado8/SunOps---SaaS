from decimal import Decimal
from typing import List
from .entities import Kit, ItemKit
from .value_objects import PotenciaWatts

class CalculadoraGeracao:
    """Domain Service: Cálculo de geração solar (RN01-04)"""
    
    FATOR_GERACAO = Decimal("0.7")
    HORAS_SOL_MES = Decimal("126")
    
    @staticmethod
    def calcular_kwp_total(itens: List[ItemKit]) -> Decimal:
        """Calcula kWp total dos painéis"""
        total_watts = sum(
            item.potencia.valor * item.quantidade.valor
            for item in itens
            if item.eh_painel_solar() and item.potencia
        )
        return Decimal(total_watts) / Decimal(1000)
    
    @staticmethod
    def calcular_kwh_mes(kwp: Decimal) -> Decimal:
        """RN01: Geração = Potência × 0.7 × 126 kWh/mês"""
        return kwp * CalculadoraGeracao.FATOR_GERACAO * CalculadoraGeracao.HORAS_SOL_MES

class ValidadorKit:
    """Domain Service: Validação de kits (RN05)"""
    
    MIN_CATEGORIAS = 2
    
    @staticmethod
    def validar(kit: Kit) -> bool:
        """RN05: Kit exige mínimo 2 categorias diferentes"""
        return len(kit.obter_categorias_unicas()) >= ValidadorKit.MIN_CATEGORIAS
