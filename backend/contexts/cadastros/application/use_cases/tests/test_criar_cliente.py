"""
Testes para Use Case CriarCliente
"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent))

from contexts.cadastros.application.use_cases import CriarClienteUseCase
from contexts.cadastros.application.dtos.criar_cliente_dto import CriarClienteDTO
from contexts.cadastros.infrastructure.repositories.cliente_repository_memory import ClienteRepositoryInMemory


def test_criar_cliente_com_cpf():
    """Deve criar cliente com CPF"""
    repository = ClienteRepositoryInMemory()
    use_case = CriarClienteUseCase(repository)
    
    dto = CriarClienteDTO(
        nome="João Silva",
        documento="12345678909",
        email="joao@email.com",
        telefone="11987654321",
        endereco="Rua A, 123"
    )
    
    cliente = use_case.executar(dto)
    
    assert cliente.nome == "João Silva"
    assert cliente.id is not None
    assert cliente.ativo is True


def test_criar_cliente_com_cnpj():
    """Deve criar cliente com CNPJ"""
    repository = ClienteRepositoryInMemory()
    use_case = CriarClienteUseCase(repository)
    
    dto = CriarClienteDTO(
        nome="Empresa XYZ",
        documento="11222333000181",
        email="contato@empresa.com",
        telefone="1133334444",
        endereco="Av B, 456"
    )
    
    cliente = use_case.executar(dto)
    
    assert cliente.nome == "Empresa XYZ"
    assert cliente.id is not None


def test_nao_deve_criar_cliente_duplicado():
    """Não deve criar cliente com documento duplicado"""
    repository = ClienteRepositoryInMemory()
    use_case = CriarClienteUseCase(repository)
    
    dto = CriarClienteDTO(
        nome="João Silva",
        documento="12345678909",
        email="joao@email.com",
        telefone="11987654321",
        endereco="Rua A, 123"
    )
    
    # Primeiro cliente
    use_case.executar(dto)
    
    # Tentar criar duplicado
    with pytest.raises(ValueError, match="já existe"):
        use_case.executar(dto)


def test_deve_rejeitar_documento_invalido():
    """Deve rejeitar documento com tamanho inválido"""
    repository = ClienteRepositoryInMemory()
    use_case = CriarClienteUseCase(repository)
    
    dto = CriarClienteDTO(
        nome="João Silva",
        documento="123456789",  # Nem CPF nem CNPJ
        email="joao@email.com",
        telefone="11987654321",
        endereco="Rua A, 123"
    )
    
    with pytest.raises(ValueError, match="CPF.*CNPJ"):
        use_case.executar(dto)


def test_deve_rejeitar_email_invalido():
    """Deve rejeitar email inválido"""
    repository = ClienteRepositoryInMemory()
    use_case = CriarClienteUseCase(repository)
    
    dto = CriarClienteDTO(
        nome="João Silva",
        documento="12345678909",
        email="email-invalido",
        telefone="11987654321",
        endereco="Rua A, 123"
    )
    
    with pytest.raises(ValueError, match="inválido"):
        use_case.executar(dto)
