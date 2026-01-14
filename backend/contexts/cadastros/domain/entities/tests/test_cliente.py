"""
Testes para Entity Cliente
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from contexts.cadastros.domain.entities.cliente import Cliente
from shared.domain.value_objects import CPF, Email, Telefone


def test_criar_cliente_valido():
    """Deve criar cliente v\u00e1lido"""
    cliente = Cliente(
        nome="Jo\u00e3o Silva",
        documento=CPF("12345678909"),
        email=Email("joao@email.com"),
        telefone=Telefone("11987654321"),
        endereco="Rua A, 123"
    )
    
    assert cliente.nome == "Jo\u00e3o Silva"
    assert cliente.ativo is True
    assert cliente.id is not None


def test_cliente_nome_curto():
    """Deve rejeitar nome muito curto"""
    with pytest.raises(ValueError, match="3 caracteres"):
        Cliente(
            nome="Jo",
            documento=CPF("12345678909"),
            email=Email("joao@email.com"),
            telefone=Telefone("11987654321"),
            endereco="Rua A, 123"
        )


def test_cliente_sem_endereco():
    """Deve rejeitar cliente sem endere\u00e7o"""
    with pytest.raises(ValueError, match="obrigat\u00f3rio"):
        Cliente(
            nome="Jo\u00e3o Silva",
            documento=CPF("12345678909"),
            email=Email("joao@email.com"),
            telefone=Telefone("11987654321"),
            endereco=""
        )


def test_desativar_cliente():
    """Deve desativar cliente"""
    cliente = Cliente(
        nome="Jo\u00e3o Silva",
        documento=CPF("12345678909"),
        email=Email("joao@email.com"),
        telefone=Telefone("11987654321"),
        endereco="Rua A, 123"
    )
    
    cliente.desativar()
    assert cliente.ativo is False


def test_ativar_cliente():
    """Deve ativar cliente"""
    cliente = Cliente(
        nome="Jo\u00e3o Silva",
        documento=CPF("12345678909"),
        email=Email("joao@email.com"),
        telefone=Telefone("11987654321"),
        endereco="Rua A, 123"
    )
    
    cliente.desativar()
    cliente.ativar()
    assert cliente.ativo is True
