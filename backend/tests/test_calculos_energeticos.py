"""Testes para cálculos energéticos."""
import pytest
from decimal import Decimal
from contexts.orcamentos.domain.value_objects.dados_uc import (
    TipoLigacao, Tensao, ClasseTarifaria, Tarifa, 
    Localizacao, HistoricoConsumo
)
from contexts.orcamentos.domain.value_objects.hsp import HSP
from contexts.orcamentos.domain.entities.unidade_consumidora import UnidadeConsumidora
from contexts.orcamentos.domain.services.calculos_energeticos import (
    CalculadoraDimensionamento,
    CalculadoraPotenciaInstalada,
    ValidadorEletrico,
    CalculadoraGeracao,
    CalculadoraEconomia,
    CalculadoraFinanciamento,
    CalculadoraVPL,
    CalculadoraTIR,
    CalculadoraOM
)


def test_tipo_ligacao_custo_disponibilidade():
    mono = TipoLigacao(TipoLigacao.MONOFASICA)
    assert mono.custo_disponibilidade == 30
    
    bi = TipoLigacao(TipoLigacao.BIFASICA)
    assert bi.custo_disponibilidade == 50
    
    tri = TipoLigacao(TipoLigacao.TRIFASICA)
    assert tri.custo_disponibilidade == 100


def test_historico_consumo_media():
    hist = HistoricoConsumo([300, 350, 400, 380, 360, 340, 320, 330, 370, 390, 410, 350])
    assert abs(hist.media_mensal - Decimal("358.33")) < Decimal("0.01")


def test_unidade_consumidora_geracao_necessaria():
    uc = UnidadeConsumidora(
        id="uc-1",
        cliente_id="cli-1",
        historico_consumo=HistoricoConsumo([400, 400, 400]),
        tipo_ligacao=TipoLigacao(TipoLigacao.MONOFASICA),
        tensao=Tensao(220),
        classe_tarifaria=ClasseTarifaria("B1"),
        tarifa=Tarifa(Decimal("0.50"), Decimal("0.30")),
        localizacao=Localizacao(-23.5505, -46.6333, "São Paulo")
    )
    
    assert uc.consumo_medio == Decimal("400")
    assert uc.geracao_necessaria == Decimal("370")  # 400 - 30


def test_calculadora_dimensionamento():
    hsp = HSP(Decimal("5.0"), "CRESESB")
    potencia = CalculadoraDimensionamento.calcular_potencia_sistema(
        geracao_necessaria=Decimal("370"),
        hsp=hsp,
        fator_perdas=Decimal("0.80")
    )
    # 370 / (5.0 × 30 × 0.80) = 370 / 120 = 3.083 kWp
    assert potencia == Decimal("3.083333333333333333333333333")


def test_calculadora_potencia_instalada():
    potencia = CalculadoraPotenciaInstalada.calcular(
        qtd_modulos=8,
        potencia_modulo=Decimal("0.550")
    )
    assert potencia == Decimal("4.400")


def test_dc_ac_ratio():
    ratio = CalculadoraPotenciaInstalada.calcular_dc_ac_ratio(
        potencia_instalada=Decimal("4.4"),
        potencia_inversor=Decimal("4.0")
    )
    assert ratio == Decimal("1.1")
    assert CalculadoraPotenciaInstalada.validar_dc_ac_ratio(ratio) is True


def test_validador_eletrico():
    assert ValidadorEletrico.validar_tensao_string(
        tensao_string=Decimal("400"),
        vmax_inversor=Decimal("600"),
        vmin_mppt=Decimal("150")
    ) is True
    
    assert ValidadorEletrico.validar_corrente(
        corrente=Decimal("10"),
        imax_inversor=Decimal("12")
    ) is True


def test_calculadora_geracao():
    hsp = HSP(Decimal("5.0"), "CRESESB")
    geracao_mensal = CalculadoraGeracao.calcular_geracao_mensal(
        potencia_instalada=Decimal("4.4"),
        hsp=hsp,
        fator_perdas=Decimal("0.80")
    )
    # 4.4 × 5.0 × 30 × 0.80 = 528 kWh/mês
    assert geracao_mensal == Decimal("528.0")
    
    geracao_anual = CalculadoraGeracao.calcular_geracao_anual(geracao_mensal)
    assert geracao_anual == Decimal("6336.0")


def test_geracao_com_degradacao():
    geracao_ano_5 = CalculadoraGeracao.calcular_geracao_com_degradacao(
        geracao_ano_1=Decimal("6336"),
        ano=5,
        taxa_degradacao=Decimal("0.007")
    )
    # 6336 × (1 - 0.007)^5 = 6336 × 0.965 ≈ 6117
    assert 6100 < geracao_ano_5 < 6120


def test_calculadora_economia():
    economia_mensal = CalculadoraEconomia.calcular_economia_mensal(
        geracao_mensal=Decimal("528"),
        tarifa_kwh=Decimal("0.80")
    )
    assert economia_mensal == Decimal("422.40")
    
    payback = CalculadoraEconomia.calcular_payback_simples(
        custo_total=Decimal("20000"),
        economia_anual=Decimal("5068.80")
    )
    # 20000 / 5068.80 ≈ 3.95 anos
    assert 3.9 < payback < 4.0


def test_economia_com_fio_b():
    economia = CalculadoraEconomia.calcular_economia_com_fio_b(
        geracao=Decimal("528"),
        tarifa=Decimal("0.80"),
        percentual_fio_b=Decimal("0.15")  # 15% Fio B
    )
    # 528 × (0.80 - 0.12) = 528 × 0.68 = 359.04
    assert economia == Decimal("359.04")


def test_calculadora_financiamento():
    parcela = CalculadoraFinanciamento.calcular_parcela(
        valor_financiado=Decimal("20000"),
        taxa_juros_mensal=Decimal("0.01"),  # 1% a.m.
        num_parcelas=60
    )
    # PMT ≈ 444.89
    assert 440 < parcela < 450
    
    delta = CalculadoraFinanciamento.calcular_delta_mensal(
        economia_mensal=Decimal("422.40"),
        parcela=parcela
    )
    assert CalculadoraFinanciamento.eh_viavel(delta) is False  # Parcela > economia


def test_calculadora_vpls():
    fluxos = [Decimal("5000")] * 25  # 25 anos de economia
    vpls = CalculadoraVPL.calcular(
        custo_inicial=Decimal("20000"),
        fluxos_caixa=fluxos,
        taxa_desconto=Decimal("0.08")
    )
    assert vpls > 0  # VPL positivo = investimento viável


def test_calculadora_tir_fluxo():
    fluxos = CalculadoraTIR.calcular_fluxo_caixa(
        custo_inicial=Decimal("20000"),
        economia_anual=Decimal("5000"),
        custo_om_anual=Decimal("200"),
        anos=25
    )
    assert len(fluxos) == 26  # FC0 + 25 anos
    assert fluxos[0] == Decimal("-20000")
    assert fluxos[1] == Decimal("4800")  # 5000 - 200


def test_calculadora_om():
    om = CalculadoraOM.calcular_anual(
        custo_sistema=Decimal("20000"),
        percentual=Decimal("0.01")
    )
    assert om == Decimal("200")
