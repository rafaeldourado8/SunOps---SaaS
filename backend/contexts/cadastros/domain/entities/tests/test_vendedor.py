"""
Testes para Entity Vendedor
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from contexts.cadastros.domain.entities.vendedor import Vendedor
from shared.domain.value_objects import Email, Telefone


def test_criar_vendedor_valido():
    """Deve criar vendedor válido"""
    vendedor = Vendedor(
        nome="Carlos Vendas",
        email=Email("carlos@empresa.com"),
        telefone=Telefone("11987654321")
    )
    
    assert vendedor.nome == "Carlos Vendas"
    assert vendedor.ativo is True
    assert vendedor.comissao_percentual == 5.0
    assert vendedor.id is not None


def test_vendedor_com_comissao_customizada():
    """Deve criar vendedor com comissão customizada"""
    vendedor = Vendedor(
        nome="Carlos Vendas",
        email=Email("carlos@empresa.com"),
        telefone=Telefone("11987654321"),
        comissao_percentual=10.0
    )
    
    assert vendedor.comissao_percentual == 10.0


def test_vendedor_nome_curto():
    """Deve rejeitar nome muito curto"""
    with pytest.raises(ValueError, match="3 caracteres"):
        Vendedor(
            nome="Ca",
            email=Email("carlos@empresa.com"),
            telefone=Telefone("11987654321")
        )


def test_vendedor_comissao_negativa():
    """Deve rejeitar comissão negativa"""
    with pytest.raises(ValueError, match="entre 0 e 100"):
        Vendedor(
            nome="Carlos Vendas",
            email=Email("carlos@empresa.com"),
            telefone=Telefone("11987654321"),
            comissao_percentual=-5.0
        )


def test_vendedor_comissao_acima_100():
    """Deve rejeitar comissão acima de 100%"""
    with pytest.raises(ValueError, match="entre 0 e 100"):
        Vendedor(
            nome="Carlos Vendas",
            email=Email("carlos@empresa.com"),
            telefone=Telefone("11987654321"),
            comissao_percentual=150.0
        )


def test_atualizar_comissao():
    """Deve atualizar comissão do vendedor"""
    vendedor = Vendedor(
        nome="Carlos Vendas",
        email=Email("carlos@empresa.com"),
        telefone=Telefone("11987654321")
    )
    
    vendedor.atualizar_comissao(8.0)
    assert vendedor.comissao_percentual == 8.0


def test_atualizar_comissao_invalida():
    """Deve rejeitar atualização de comissão inválida"""
    vendedor = Vendedor(
        nome="Carlos Vendas",
        email=Email("carlos@empresa.com"),
        telefone=Telefone("11987654321")
    )
    
    with pytest.raises(ValueError, match="entre 0 e 100"):
        vendedor.atualizar_comissao(150.0)


def test_calcular_comissao():
    """Deve calcular comissão corretamente"""
    vendedor = Vendedor(
        nome="Carlos Vendas",
        email=Email("carlos@empresa.com"),
        telefone=Telefone("11987654321"),
        comissao_percentual=10.0
    )
    
    comissao = vendedor.calcular_comissao(10000.0)
    assert comissao == 1000.0


def test_desativar_vendedor():
    """Deve desativar vendedor"""
    vendedor = Vendedor(
        nome="Carlos Vendas",
        email=Email("carlos@empresa.com"),
        telefone=Telefone("11987654321")
    )
    
    vendedor.desativar()
    assert vendedor.ativo is False


def test_ativar_vendedor():
    """Deve ativar vendedor"""
    vendedor = Vendedor(
        nome="Carlos Vendas",
        email=Email("carlos@empresa.com"),
        telefone=Telefone("11987654321")
    )
    
    vendedor.desativar()
    vendedor.ativar()
    assert vendedor.ativo is True
