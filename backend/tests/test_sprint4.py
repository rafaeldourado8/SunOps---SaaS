"""
Testes Sprint 4
"""
import pytest
from decimal import Decimal
from contexts.orcamentos.domain.entities.kit import Kit, ItemKit
from contexts.orcamentos.domain.entities.orcamento import Orcamento
from contexts.orcamentos.domain.services.calculadora_geracao import CalculadoraGeracao
from contexts.orcamentos.domain.services.calculadora_payback import CalculadoraPayback


def test_criar_kit():
    kit = Kit(nome="Kit Residencial 5kWp")
    item = ItemKit(
        produto_id=1,
        produto_nome="Painel 550W",
        quantidade=10,
        preco_unitario=Decimal("800.00")
    )
    kit.adicionar_item(item)
    
    assert kit.quantidade_itens == 1
    assert kit.preco_total == Decimal("8000.00")


def test_remover_item_kit():
    kit = Kit(nome="Kit")
    kit.adicionar_item(ItemKit(1, "Painel", 10, Decimal("800")))
    kit.remover_item(1)
    
    assert kit.quantidade_itens == 0


def test_criar_orcamento():
    kit = Kit(nome="Kit 5kWp")
    orcamento = Orcamento(
        cliente_id=1,
        vendedor_id=1,
        kit=kit,
        valor_total=Decimal("25000.00")
    )
    
    assert orcamento.status == "RASCUNHO"
    assert orcamento.valor_total == Decimal("25000.00")


def test_orcamento_enviar():
    kit = Kit(nome="Kit")
    orcamento = Orcamento(1, 1, kit, Decimal("25000"))
    orcamento.enviar()
    
    assert orcamento.status == "ENVIADO"


def test_calculadora_geracao():
    geracao = CalculadoraGeracao.calcular(
        potencia_kwp=Decimal("5.0"),
        hsp=Decimal("5.0")
    )
    
    # 5 kWp × 5 HSP × 30 dias × 0.8 = 600 kWh/mês
    assert geracao == Decimal("600.00")


def test_calculadora_payback():
    payback = CalculadoraPayback.calcular(
        investimento=Decimal("25000.00"),
        economia_mensal=Decimal("500.00")
    )
    
    # 25000 / 500 = 50 meses
    assert payback == Decimal("50.00")
