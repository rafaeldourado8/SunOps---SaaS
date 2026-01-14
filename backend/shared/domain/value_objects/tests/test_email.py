"""
Testes para Value Object Email
"""
import pytest
import sys
sys.path.append('../../../..')
from shared.domain.value_objects.email import Email


def test_email_valido():
    """Deve aceitar email v\u00e1lido"""
    email = Email("joao@email.com")
    assert email.valor == "joao@email.com"


def test_email_converte_minuscula():
    """Deve converter email para min\u00fascula"""
    email = Email("JOAO@EMAIL.COM")
    assert email.valor == "joao@email.com"


def test_email_remove_espacos():
    """Deve remover espa\u00e7os"""
    email = Email("  joao@email.com  ")
    assert email.valor == "joao@email.com"


def test_email_vazio():
    """Deve rejeitar email vazio"""
    with pytest.raises(ValueError, match="vazio"):
        Email("")


def test_email_sem_arroba():
    """Deve rejeitar email sem @"""
    with pytest.raises(ValueError, match="inv\u00e1lido"):
        Email("joaoemail.com")


def test_email_sem_dominio():
    """Deve rejeitar email sem dom\u00ednio"""
    with pytest.raises(ValueError, match="inv\u00e1lido"):
        Email("joao@")


def test_email_igualdade():
    """Dois emails iguais devem ser iguais"""
    email1 = Email("joao@email.com")
    email2 = Email("JOAO@EMAIL.COM")
    assert email1 == email2
