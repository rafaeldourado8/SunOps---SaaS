"""Calculadora financeira com governança."""
from decimal import Decimal
import math
from typing import Dict
from ..config_financeira import CONFIG_FINANCEIRA


class CalculadoraFinanceiraGovernada:
    """Calcula preços com governança financeira."""
    
    @staticmethod
    def calcular_custo_total(custo_equipamentos: Decimal, qtd_modulos: int) -> Decimal:
        custo_montagem = Decimal(qtd_modulos) * CONFIG_FINANCEIRA.CUSTO_MONTAGEM_POR_PAINEL
        return custo_equipamentos + custo_montagem + CONFIG_FINANCEIRA.CUSTO_OPERACIONAL_FIXO
    
    @staticmethod
    def calcular_preco_minimo(custo_total: Decimal) -> Decimal:
        """Formula: custo_total / (1 - percentual_total)"""
        return custo_total / (Decimal("1") - CONFIG_FINANCEIRA.percentual_total)
    
    @staticmethod
    def arredondar_preco(preco: Decimal) -> Decimal:
        multiplo = CONFIG_FINANCEIRA.ARREDONDAMENTO_MULTIPLO
        return Decimal(math.ceil(float(preco) / multiplo) * multiplo)
    
    @staticmethod
    def calcular_quebra_financeira(preco_venda: Decimal, custo_total: Decimal) -> Dict:
        comissao = preco_venda * CONFIG_FINANCEIRA.COMISSAO_PERCENTUAL
        imposto = preco_venda * CONFIG_FINANCEIRA.IMPOSTO_PERCENTUAL
        lucro_liquido = preco_venda - custo_total - comissao - imposto
        margem_real = lucro_liquido / preco_venda if preco_venda > 0 else Decimal("0")
        
        return {
            "comissao": comissao.quantize(Decimal("0.01")),
            "imposto": imposto.quantize(Decimal("0.01")),
            "lucro_liquido": lucro_liquido.quantize(Decimal("0.01")),
            "margem_real": margem_real
        }
    
    @staticmethod
    def calcular_preco_completo(custo_equipamentos: Decimal, qtd_modulos: int) -> Dict:
        """ADMIN VIEW - Todos os dados."""
        custo_total = CalculadoraFinanceiraGovernada.calcular_custo_total(custo_equipamentos, qtd_modulos)
        preco_minimo = CalculadoraFinanceiraGovernada.calcular_preco_minimo(custo_total)
        preco_final = CalculadoraFinanceiraGovernada.arredondar_preco(preco_minimo)
        quebra = CalculadoraFinanceiraGovernada.calcular_quebra_financeira(preco_final, custo_total)
        
        return {
            "custo_total": float(custo_total),
            "custo_equipamentos": float(custo_equipamentos),
            "custo_montagem": float(Decimal(qtd_modulos) * CONFIG_FINANCEIRA.CUSTO_MONTAGEM_POR_PAINEL),
            "custo_operacional": float(CONFIG_FINANCEIRA.CUSTO_OPERACIONAL_FIXO),
            "preco_minimo": float(preco_minimo),
            "preco_final": float(preco_final),
            "comissao": float(quebra["comissao"]),
            "imposto": float(quebra["imposto"]),
            "lucro_liquido": float(quebra["lucro_liquido"]),
            "margem_real": float(quebra["margem_real"]),
            "margem_valida": quebra["margem_real"] >= CONFIG_FINANCEIRA.MARGEM_LUCRO_MINIMA
        }
    
    @staticmethod
    def calcular_preco_vendedor(custo_equipamentos: Decimal, qtd_modulos: int) -> Dict:
        """VENDEDOR VIEW - Apenas preço final."""
        resultado = CalculadoraFinanceiraGovernada.calcular_preco_completo(custo_equipamentos, qtd_modulos)
        return {
            "preco_final": resultado["preco_final"],
            "parcelas_sugeridas": 120,
            "valor_parcela": round(resultado["preco_final"] / 120, 2)
        }
