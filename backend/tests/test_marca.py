"""
Testes para Marca
"""
import pytest
from contexts.catalogo.domain.entities.marca import Marca


def test_criar_marca_valida():
    marca = Marca(nome="Canadian Solar")
    
    assert marca.nome == "Canadian Solar"
    assert marca.ativo is True


def test_marca_nome_curto():
    with pytest.raises(ValueError, match="Nome deve ter no mínimo 2 caracteres"):
        Marca(nome="A")


def test_marca_ativar_desativar():
    marca = Marca(nome="Jinko Solar")
    
    marca.desativar()
    assert marca.ativo is False
    
    marca.ativar()
    assert marca.ativo is True
