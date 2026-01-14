"""
Testes para Fornecedor
"""
import pytest
from contexts.cadastros.domain.entities.fornecedor import Fornecedor
from shared.domain.value_objects.cnpj import CNPJ
from shared.domain.value_objects.email import Email
from shared.domain.value_objects.telefone import Telefone


def test_criar_fornecedor_valido():
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        cnpj=CNPJ("11222333000181"),
        email=Email("fornecedor@test.com"),
        telefone=Telefone("11999999999")
    )
    
    assert fornecedor.nome == "Fornecedor Teste"
    assert fornecedor.ativo is True


def test_fornecedor_nome_curto():
    with pytest.raises(ValueError, match="Nome deve ter no mínimo 3 caracteres"):
        Fornecedor(
            nome="AB",
            cnpj=CNPJ("11222333000181"),
            email=Email("test@test.com"),
            telefone=Telefone("11999999999")
        )


def test_fornecedor_ativar_desativar():
    fornecedor = Fornecedor(
        nome="Fornecedor Teste",
        cnpj=CNPJ("11222333000181"),
        email=Email("test@test.com"),
        telefone=Telefone("11999999999")
    )
    
    fornecedor.desativar()
    assert fornecedor.ativo is False
    
    fornecedor.ativar()
    assert fornecedor.ativo is True
