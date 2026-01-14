"""
Use Case: Criar Cliente

Clean Architecture: Application Layer
SOLID: 
- Single Responsibility: Apenas criar cliente
- Dependency Inversion: Depende de ClienteRepository (abstração)
Complexidade Ciclomática: 3
"""
import sys
sys.path.append('../../..')

from contexts.cadastros.domain.entities import Cliente
from contexts.cadastros.domain.repositories import ClienteRepository
from contexts.cadastros.application.dtos.criar_cliente_dto import CriarClienteDTO
from shared.domain.value_objects import CPF, CNPJ, Email, Telefone


class CriarClienteUseCase:
    """
    Use Case para criar um novo cliente.
    
    Responsabilidades:
    1. Validar se documento já existe
    2. Criar Value Objects
    3. Criar Entity Cliente
    4. Persistir via Repository
    """
    
    def __init__(self, repository: ClienteRepository):
        """
        Injeção de Dependência (SOLID - D).
        Complexidade: 1
        """
        self.repository = repository
    
    def executar(self, dto: CriarClienteDTO) -> Cliente:
        """
        Executa o caso de uso.
        Complexidade: 3 (3 ifs)
        
        Args:
            dto: Dados para criar cliente
            
        Returns:
            Cliente criado
            
        Raises:
            ValueError: Se documento já existe ou dados inválidos
        """
        # Validar se documento já existe
        cliente_existente = self.repository.buscar_por_documento(dto.documento)
        if cliente_existente:
            raise ValueError(f"Cliente com documento {dto.documento} já existe")
        
        # Criar Value Objects (validação automática)
        documento = self._criar_documento(dto.documento)
        email = Email(dto.email)
        telefone = Telefone(dto.telefone)
        
        # Criar Entity
        cliente = Cliente(
            nome=dto.nome,
            documento=documento,
            email=email,
            telefone=telefone,
            endereco=dto.endereco
        )
        
        # Persistir
        return self.repository.salvar(cliente)
    
    def _criar_documento(self, documento: str):
        """
        Cria CPF ou CNPJ baseado no tamanho.
        Complexidade: 2 (2 ifs)
        """
        limpo = ''.join(c for c in documento if c.isdigit())
        
        if len(limpo) == 11:
            return CPF(documento)
        elif len(limpo) == 14:
            return CNPJ(documento)
        else:
            raise ValueError("Documento deve ser CPF (11 dígitos) ou CNPJ (14 dígitos)")
