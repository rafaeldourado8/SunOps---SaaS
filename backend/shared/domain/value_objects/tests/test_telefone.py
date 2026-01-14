"""
Testes para Value Object Telefone
"""
import pytest
import sys
sys.path.append('../../../..')
from shared.domain.value_objects.telefone import Telefone


def test_telefone_valido_11_digitos():
    """Deve aceitar telefone com 11 dígitos (celular)"""
    telefone = Telefone("11987654321")
    assert telefone.valor == "11987654321"


def test_telefone_valido_10_digitos():
    """Deve aceitar telefone com 10 dígitos (fixo)"""
    telefone = Telefone("1133334444")
    assert telefone.valor == "1133334444"


def test_telefone_com_formatacao():
    """Deve aceitar telefone com formatação"""
    telefone = Telefone("(11) 98765-4321")
    assert telefone.valor == "11987654321"


def test_telefone_formatado_11_digitos():
    """Deve formatar telefone de 11 dígitos"""
    telefone = Telefone("11987654321")
    assert telefone.formatado == "(11) 98765-4321"


def test_telefone_formatado_10_digitos():
    """Deve formatar telefone de 10 dígitos"""
    telefone = Telefone("1133334444")
    assert telefone.formatado == "(11) 3333-4444"


def test_telefone_invalido_curto():
    """Deve rejeitar telefone muito curto"""
    with pytest.raises(ValueError, match="10 ou 11 dígitos"):
        Telefone("123456789")


def test_telefone_invalido_longo():
    """Deve rejeitar telefone muito longo"""
    with pytest.raises(ValueError, match="10 ou 11 dígitos"):
        Telefone("123456789012")


def test_telefone_invalido_repetidos():
    """Deve rejeitar telefone com dígitos repetidos"""
    with pytest.raises(ValueError, match="inválido"):
        Telefone("11111111111")


def test_telefone_igualdade():
    """Dois telefones iguais devem ser iguais"""
    tel1 = Telefone("11987654321")
    tel2 = Telefone("(11) 98765-4321")
    assert tel1 == tel2


def test_telefone_hash():
    """Telefone deve ser hashável"""
    telefone = Telefone("11987654321")
    assert hash(telefone) == hash(telefone.valor)


def test_telefone_str():
    """Deve retornar telefone formatado como string"""
    telefone = Telefone("11987654321")
    assert str(telefone) == "(11) 98765-4321"
