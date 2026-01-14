"""
Testes para Value Object CNPJ
"""
import pytest
import sys
sys.path.append('../../../..')
from shared.domain.value_objects.cnpj import CNPJ


def test_cnpj_valido_sem_formatacao():
    """Deve aceitar CNPJ válido sem formatação"""
    cnpj = CNPJ("11222333000181")
    assert cnpj.valor == "11222333000181"


def test_cnpj_valido_com_formatacao():
    """Deve aceitar CNPJ válido com formatação"""
    cnpj = CNPJ("11.222.333/0001-81")
    assert cnpj.valor == "11222333000181"


def test_cnpj_formatado():
    """Deve formatar CNPJ corretamente"""
    cnpj = CNPJ("11222333000181")
    assert cnpj.formatado == "11.222.333/0001-81"


def test_cnpj_invalido_tamanho():
    """Deve rejeitar CNPJ com tamanho inválido"""
    with pytest.raises(ValueError, match="14 dígitos"):
        CNPJ("123456789")


def test_cnpj_invalido_digitos_repetidos():
    """Deve rejeitar CNPJ com dígitos repetidos"""
    with pytest.raises(ValueError, match="inválido"):
        CNPJ("11111111111111")


def test_cnpj_invalido_digito_verificador():
    """Deve rejeitar CNPJ com dígito verificador inválido"""
    with pytest.raises(ValueError, match="inválido"):
        CNPJ("11222333000180")


def test_cnpj_igualdade():
    """Dois CNPJs iguais devem ser iguais"""
    cnpj1 = CNPJ("11222333000181")
    cnpj2 = CNPJ("11.222.333/0001-81")
    assert cnpj1 == cnpj2


def test_cnpj_hash():
    """CNPJ deve ser hashável"""
    cnpj = CNPJ("11222333000181")
    assert hash(cnpj) == hash(cnpj.valor)


def test_cnpj_str():
    """Deve retornar CNPJ formatado como string"""
    cnpj = CNPJ("11222333000181")
    assert str(cnpj) == "11.222.333/0001-81"
