import pytest
from decimal import Decimal
from src.core.domain.orcamentos.value_objects import Dinheiro, Quantidade, PotenciaWatts
from src.core.domain.orcamentos.exceptions import ValorInvalidoException, QuantidadeInvalidaException

class TestDinheiro:
    
    def test_criar_dinheiro_valido(self):
        dinheiro = Dinheiro(Decimal("100.00"))
        assert dinheiro.valor == Decimal("100.00")
    
    def test_dinheiro_negativo_deve_falhar(self):
        with pytest.raises(ValorInvalidoException):
            Dinheiro(Decimal("-10.00"))
    
    def test_multiplicar_dinheiro(self):
        dinheiro = Dinheiro(Decimal("50.00"))
        resultado = dinheiro.multiplicar(3)
        assert resultado.valor == Decimal("150.00")
    
    def test_somar_dinheiro(self):
        d1 = Dinheiro(Decimal("100.00"))
        d2 = Dinheiro(Decimal("50.00"))
        resultado = d1.somar(d2)
        assert resultado.valor == Decimal("150.00")

class TestQuantidade:
    
    def test_criar_quantidade_valida(self):
        qtd = Quantidade(5)
        assert qtd.valor == 5
    
    def test_quantidade_zero_deve_falhar(self):
        with pytest.raises(QuantidadeInvalidaException):
            Quantidade(0)
    
    def test_quantidade_negativa_deve_falhar(self):
        with pytest.raises(QuantidadeInvalidaException):
            Quantidade(-1)

class TestPotenciaWatts:
    
    def test_criar_potencia_valida(self):
        potencia = PotenciaWatts(550)
        assert potencia.valor == 550
    
    def test_converter_para_kwp(self):
        potencia = PotenciaWatts(5500)
        assert potencia.para_kwp() == Decimal("5.5")
    
    def test_potencia_zero_deve_falhar(self):
        with pytest.raises(ValorInvalidoException):
            PotenciaWatts(0)
