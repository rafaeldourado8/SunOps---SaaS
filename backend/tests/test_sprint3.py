"""
Testes Sprint 3
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from contexts.catalogo.domain.value_objects.preco import Preco
from contexts.catalogo.domain.entities.painel import Painel
from contexts.catalogo.domain.entities.inversor import Inversor


def test_preco_validade_3_dias_uteis():
    # Sexta-feira
    data_cotacao = datetime(2024, 1, 5, 10, 0)  # Sexta
    preco = Preco(valor=Decimal("1000.00"), data_cotacao=data_cotacao)
    
    # Validade deve ser quarta (pula sábado e domingo)
    assert preco.data_validade.weekday() == 2  # Quarta


def test_preco_esta_valido():
    preco = Preco(valor=Decimal("1000.00"), data_cotacao=datetime.now())
    assert preco.esta_valido is True


def test_criar_painel_valido():
    painel = Painel(
        nome="Painel 550W",
        marca_id=1,
        fornecedor_id=1,
        preco=Decimal("800.00"),
        potencia=Decimal("550"),
        eficiencia=Decimal("21.5"),
        tipo="MONOCRISTALINO"
    )
    
    assert painel.nome == "Painel 550W"
    assert painel.potencia == Decimal("550")


def test_painel_potencia_invalida():
    with pytest.raises(ValueError, match="Potência deve ser maior que zero"):
        Painel(
            nome="Painel",
            marca_id=1,
            fornecedor_id=1,
            preco=Decimal("800"),
            potencia=Decimal("0")
        )


def test_criar_inversor_valido():
    inversor = Inversor(
        nome="Inversor 5kW",
        marca_id=1,
        fornecedor_id=1,
        preco=Decimal("3000.00"),
        potencia=Decimal("5"),
        tipo="STRING",
        fases=1
    )
    
    assert inversor.nome == "Inversor 5kW"
    assert inversor.fases == 1


def test_inversor_fases_invalida():
    with pytest.raises(ValueError, match="Fases deve ser 1 ou 3"):
        Inversor(
            nome="Inversor",
            marca_id=1,
            fornecedor_id=1,
            preco=Decimal("3000"),
            potencia=Decimal("5"),
            fases=2
        )
