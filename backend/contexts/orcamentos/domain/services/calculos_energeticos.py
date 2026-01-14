"""Services de cálculos energéticos profissionais."""
from decimal import Decimal
from typing import List
from ..value_objects.hsp import HSP
from ..entities.unidade_consumidora import UnidadeConsumidora


class CalculadoraDimensionamento:
    """Calcula potência necessária do sistema."""
    
    FATOR_PERDAS_MIN = Decimal("0.75")
    FATOR_PERDAS_MAX = Decimal("0.82")
    FATOR_PERDAS_PADRAO = Decimal("0.80")
    
    @staticmethod
    def calcular_potencia_sistema(
        geracao_necessaria: Decimal,
        hsp: HSP,
        fator_perdas: Decimal = FATOR_PERDAS_PADRAO
    ) -> Decimal:
        """
        Calcula potência do sistema em kWp.
        Formula: potencia_kWp = geracao_necessaria / (HSP × 30 × fator_perdas)
        """
        if not (CalculadoraDimensionamento.FATOR_PERDAS_MIN <= fator_perdas <= CalculadoraDimensionamento.FATOR_PERDAS_MAX):
            raise ValueError(f"Fator de perdas deve estar entre {CalculadoraDimensionamento.FATOR_PERDAS_MIN} e {CalculadoraDimensionamento.FATOR_PERDAS_MAX}")
        
        denominador = hsp.valor * Decimal("30") * fator_perdas
        return geracao_necessaria / denominador


class CalculadoraPotenciaInstalada:
    """Calcula potência instalada real."""
    
    @staticmethod
    def calcular(qtd_modulos: int, potencia_modulo: Decimal) -> Decimal:
        """
        Potência instalada = qtd_modulos × potencia_modulo
        """
        return Decimal(qtd_modulos) * potencia_modulo
    
    @staticmethod
    def calcular_dc_ac_ratio(potencia_instalada: Decimal, potencia_inversor: Decimal) -> Decimal:
        """
        Relação DC/AC = potencia_instalada / potencia_inversor
        Ideal: 1.10 ≤ DC/AC ≤ 1.30
        """
        return potencia_instalada / potencia_inversor
    
    @staticmethod
    def validar_dc_ac_ratio(ratio: Decimal) -> bool:
        """Valida se ratio está na faixa ideal."""
        return Decimal("1.10") <= ratio <= Decimal("1.30")


class ValidadorEletrico:
    """Valida parâmetros elétricos do sistema."""
    
    @staticmethod
    def validar_tensao_string(
        tensao_string: Decimal,
        vmax_inversor: Decimal,
        vmin_mppt: Decimal
    ) -> bool:
        """
        Valida:
        - tensão máxima string < Vmax inversor
        - tensão mínima MPPT > Vmin inversor
        """
        return tensao_string < vmax_inversor and tensao_string > vmin_mppt
    
    @staticmethod
    def validar_corrente(corrente: Decimal, imax_inversor: Decimal) -> bool:
        """Valida corrente < Imax inversor."""
        return corrente < imax_inversor


class CalculadoraGeracao:
    """Calcula geração estimada do sistema."""
    
    @staticmethod
    def calcular_geracao_mensal(
        potencia_instalada: Decimal,
        hsp: HSP,
        fator_perdas: Decimal = Decimal("0.80")
    ) -> Decimal:
        """
        Geração mensal = potencia_instalada × HSP × 30 × fator_perdas
        """
        return potencia_instalada * hsp.valor * Decimal("30") * fator_perdas
    
    @staticmethod
    def calcular_geracao_anual(geracao_mensal: Decimal) -> Decimal:
        """Geração anual = geracao_mensal × 12"""
        return geracao_mensal * Decimal("12")
    
    @staticmethod
    def calcular_geracao_com_degradacao(
        geracao_ano_1: Decimal,
        ano: int,
        taxa_degradacao: Decimal = Decimal("0.007")
    ) -> Decimal:
        """
        Geração com degradação = geracao_ano_1 × (1 - degradacao)^ano
        Taxa padrão: 0.7% ao ano
        """
        return geracao_ano_1 * ((Decimal("1") - taxa_degradacao) ** ano)


class CalculadoraEconomia:
    """Calcula economia e retorno financeiro."""
    
    @staticmethod
    def calcular_economia_mensal(geracao_mensal: Decimal, tarifa_kwh: Decimal) -> Decimal:
        """Economia mensal = geracao_mensal × tarifa_kWh"""
        return geracao_mensal * tarifa_kwh
    
    @staticmethod
    def calcular_economia_anual(economia_mensal: Decimal) -> Decimal:
        """Economia anual = economia_mensal × 12"""
        return economia_mensal * Decimal("12")
    
    @staticmethod
    def calcular_payback_simples(custo_total: Decimal, economia_anual: Decimal) -> Decimal:
        """Payback simples = custo_total / economia_anual (em anos)"""
        return custo_total / economia_anual
    
    @staticmethod
    def calcular_economia_com_fio_b(
        geracao: Decimal,
        tarifa: Decimal,
        percentual_fio_b: Decimal
    ) -> Decimal:
        """
        Economia real considerando Lei 14.300 (Fio B progressivo).
        economia_real = geracao × (tarifa - fioB)
        """
        fio_b = tarifa * percentual_fio_b
        return geracao * (tarifa - fio_b)


class CalculadoraFinanciamento:
    """Calcula parcelas e viabilidade de financiamento."""
    
    @staticmethod
    def calcular_parcela(
        valor_financiado: Decimal,
        taxa_juros_mensal: Decimal,
        num_parcelas: int
    ) -> Decimal:
        """
        PMT = financiamento × i / (1 - (1 + i)^-n)
        """
        i = taxa_juros_mensal
        n = num_parcelas
        return valor_financiado * i / (Decimal("1") - (Decimal("1") + i) ** -n)
    
    @staticmethod
    def calcular_delta_mensal(economia_mensal: Decimal, parcela: Decimal) -> Decimal:
        """Delta mensal = economia_mensal - parcela"""
        return economia_mensal - parcela
    
    @staticmethod
    def eh_viavel(delta_mensal: Decimal) -> bool:
        """Financiamento é viável se parcela < economia."""
        return delta_mensal > 0


class CalculadoraVPL:
    """Calcula VPL (Valor Presente Líquido)."""
    
    @staticmethod
    def calcular(
        custo_inicial: Decimal,
        fluxos_caixa: List[Decimal],
        taxa_desconto: Decimal
    ) -> Decimal:
        """
        VPL = -custo_inicial + Σ (FCt / (1 + taxa)^t)
        """
        vpls = [-custo_inicial]
        for t, fc in enumerate(fluxos_caixa, start=1):
            vpls.append(fc / ((Decimal("1") + taxa_desconto) ** t))
        return sum(vpls)


class CalculadoraTIR:
    """Calcula TIR (Taxa Interna de Retorno)."""
    
    @staticmethod
    def calcular_fluxo_caixa(
        custo_inicial: Decimal,
        economia_anual: Decimal,
        custo_om_anual: Decimal,
        anos: int = 25
    ) -> List[Decimal]:
        """
        Gera fluxo de caixa para 25 anos.
        FC0 = -custo_inicial
        FC1..25 = economia_anual - O&M
        """
        fluxos = [-custo_inicial]
        for _ in range(anos):
            fluxos.append(economia_anual - custo_om_anual)
        return fluxos


class CalculadoraOM:
    """Calcula custo de O&M (Operação e Manutenção)."""
    
    @staticmethod
    def calcular_anual(
        custo_sistema: Decimal,
        percentual: Decimal = Decimal("0.01")
    ) -> Decimal:
        """
        O&M ≈ 0.5% a 1% do CAPEX / ano
        Padrão: 1%
        """
        if not (Decimal("0.005") <= percentual <= Decimal("0.01")):
            raise ValueError("Percentual O&M deve estar entre 0.5% e 1%")
        return custo_sistema * percentual
