"""Testes para motor de orçamento automático."""
import pytest
from decimal import Decimal
from contexts.orcamentos.application.dtos.orcamento_dto import InputOrcamento
from contexts.orcamentos.application.use_cases.gerar_orcamento_automatico import (
    MotorOrcamentoAutomatico
)


def test_orcamento_automatico_residencial_a_vista():
    """Teste completo: residencial, São Paulo, à vista."""
    input_data = InputOrcamento(
        cidade="São Paulo",
        consumo_mensal_kwh=400,
        tipo_ligacao="MONOFASICA",
        tipo_telhado="CERAMICO",
        forma_pagamento="A_VISTA",
        classe_tarifaria="B1"
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    # Validações básicas
    assert output.consumo_medio == Decimal("400")
    assert output.consumo_compensavel == Decimal("370")  # 400 - 30
    assert output.potencia_necessaria > 0
    
    # Kit
    assert output.kit.qtd_modulos > 0
    assert output.kit.potencia_instalada > 0
    assert output.kit.dc_ac_valido is True
    
    # Geração
    assert output.geracao_mensal > 0
    assert output.geracao_anual == output.geracao_mensal * 12
    
    # Financeiro
    assert output.financeiro.custo_total > 0
    assert output.financeiro.economia_mensal > 0
    assert output.financeiro.payback_anos > 0
    assert output.financeiro.parcela_mensal is None  # À vista
    
    # Performance
    assert output.tempo_processamento_ms < 120000  # < 2 minutos


def test_orcamento_automatico_comercial_financiado():
    """Teste: comercial, financiado."""
    input_data = InputOrcamento(
        cidade="Brasília",
        consumo_mensal_kwh=1000,
        tipo_ligacao="TRIFASICA",
        tipo_telhado="METALICO",
        forma_pagamento="FINANCIADO",
        classe_tarifaria="A4",
        taxa_juros_mensal=Decimal("0.01"),
        num_parcelas=60
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    assert output.consumo_compensavel == Decimal("900")  # 1000 - 100
    assert output.fator_perdas == Decimal("0.82")  # Comercial
    
    # Financiamento
    assert output.financeiro.parcela_mensal is not None
    assert output.financeiro.delta_mensal is not None


def test_orcamento_cidade_sem_hsp():
    """Teste: cidade sem HSP no cache."""
    input_data = InputOrcamento(
        cidade="Cidade Inexistente",
        consumo_mensal_kwh=300,
        tipo_ligacao="MONOFASICA"
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    # Deve usar HSP padrão
    assert output.hsp_utilizado == Decimal("4.5")
    assert any("HSP não encontrado" in alerta for alerta in output.alertas)


def test_orcamento_consumo_insuficiente():
    """Teste: consumo menor que custo de disponibilidade."""
    input_data = InputOrcamento(
        cidade="São Paulo",
        consumo_mensal_kwh=20,  # Menor que 30 kWh
        tipo_ligacao="MONOFASICA"
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    assert any("Consumo insuficiente" in alerta for alerta in output.alertas)
    assert output.consumo_compensavel == Decimal("100")  # Mínimo


def test_orcamento_com_override_manual():
    """Teste: override de módulo e inversor."""
    input_data = InputOrcamento(
        cidade="Rio de Janeiro",
        consumo_mensal_kwh=500,
        tipo_ligacao="BIFASICA",
        potencia_modulo_override=Decimal("0.600"),
        qtd_modulos_override=10,
        inversor_id_override="inversor-custom-5kw"
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    assert output.kit.potencia_modulo == Decimal("0.600")
    assert output.kit.qtd_modulos == 10
    assert output.kit.potencia_instalada == Decimal("6.0")


def test_validacao_dc_ac_ratio():
    """Teste: sistema ajusta DC/AC se inválido."""
    input_data = InputOrcamento(
        cidade="Fortaleza",
        consumo_mensal_kwh=800,
        tipo_ligacao="TRIFASICA"
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    # DC/AC deve estar no range ideal
    assert Decimal("1.10") <= output.kit.dc_ac_ratio <= Decimal("1.30")
    assert output.kit.dc_ac_valido is True


def test_performance_tempo_processamento():
    """Teste: orçamento gerado em menos de 2 minutos."""
    input_data = InputOrcamento(
        cidade="Curitiba",
        consumo_mensal_kwh=600,
        tipo_ligacao="BIFASICA"
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    # Meta: ≤ 120 segundos = 120.000 ms
    assert output.tempo_processamento_ms < 120000
    # Realista: deve ser < 1 segundo
    assert output.tempo_processamento_ms < 1000


def test_calculo_payback():
    """Teste: payback calculado corretamente."""
    input_data = InputOrcamento(
        cidade="Salvador",
        consumo_mensal_kwh=450,
        tipo_ligacao="MONOFASICA"
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    # Payback = custo_total / economia_anual
    payback_esperado = (
        output.financeiro.custo_total / output.financeiro.economia_anual
    )
    assert abs(output.financeiro.payback_anos - payback_esperado) < Decimal("0.01")


def test_financiamento_parcela_maior_economia():
    """Teste: alerta quando parcela > economia."""
    input_data = InputOrcamento(
        cidade="Porto Alegre",
        consumo_mensal_kwh=300,
        tipo_ligacao="MONOFASICA",
        forma_pagamento="FINANCIADO",
        taxa_juros_mensal=Decimal("0.02"),  # 2% a.m. (alto)
        num_parcelas=36
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    # Deve ter alerta
    assert any("Parcela" in alerta and "Economia" in alerta for alerta in output.alertas)
    assert output.financeiro.mes_break_even is not None
