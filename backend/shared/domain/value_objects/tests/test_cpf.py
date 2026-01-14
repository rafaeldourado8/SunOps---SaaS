"""
Testes para Value Object CPF
"""
import pytest
import sys
sys.path.append('../../../..')
from shared.domain.value_objects.cpf import CPF


def test_cpf_valido_sem_formatacao():
    """Deve aceitar CPF v\u00e1lido sem formata\u00e7\u00e3o"""
    cpf = CPF("12345678909")
    assert cpf.valor == "12345678909"


def test_cpf_valido_com_formatacao():
    """Deve aceitar CPF v\u00e1lido com formata\u00e7\u00e3o"""
    cpf = CPF("123.456.789-09")
    assert cpf.valor == "12345678909"


def test_cpf_formatado():
    """Deve formatar CPF corretamente"""
    cpf = CPF("12345678909")
    assert cpf.formatado == "123.456.789-09"


def test_cpf_invalido_tamanho():
    """Deve rejeitar CPF com tamanho inv\u00e1lido"""
    with pytest.raises(ValueError, match="11 d\u00edgitos"):
        CPF("123456789")


def test_cpf_invalido_digitos_repetidos():
    """Deve rejeitar CPF com d\u00edgitos repetidos"""
    with pytest.raises(ValueError, match="inv\u00e1lido"):
        CPF("11111111111")


def test_cpf_invalido_digito_verificador():
    """Deve rejeitar CPF com d\u00edgito verificador inv\u00e1lido"""
    with pytest.raises(ValueError, match="inv\u00e1lido"):
        CPF("12345678900")


def test_cpf_igualdade():
    """Dois CPFs iguais devem ser iguais"""
    cpf1 = CPF("12345678909")
    cpf2 = CPF("123.456.789-09")
    assert cpf1 == cpf2


def test_cpf_hash():
    """CPF deve ser hash\u00e1vel"""
    cpf = CPF("12345678909")
    assert hash(cpf) == hash(cpf.valor)
