"""
Use Case: Criar Vendedor

Clean Architecture: Application Layer
SOLID: Single Responsibility + Dependency Inversion
Complexidade Ciclomática: 2
"""
import sys
sys.path.append('../../..')

from contexts.cadastros.domain.entities import Vendedor
from contexts.cadastros.domain.repositories import VendedorRepository
from contexts.cadastros.application.dtos.criar_vendedor_dto import CriarVendedorDTO
from shared.domain.value_objects import Email, Telefone


class CriarVendedorUseCase:
    """
    Use Case para criar um novo vendedor.
    
    Responsabilidades:
    1. Validar se email já existe
    2. Criar Value Objects
    3. Criar Entity Vendedor
    4. Persistir via Repository
    """
    
    def __init__(self, repository: VendedorRepository):
        """Injeção de Dependência. Complexidade: 1"""
        self.repository = repository
    
    def executar(self, dto: CriarVendedorDTO) -> Vendedor:
        """
        Executa o caso de uso.
        Complexidade: 2
        
        Args:
            dto: Dados para criar vendedor
            
        Returns:
            Vendedor criado
            
        Raises:
            ValueError: Se email já existe ou dados inválidos
        """
        # Validar se email já existe
        vendedor_existente = self.repository.buscar_por_email(dto.email)
        if vendedor_existente:
            raise ValueError(f"Vendedor com email {dto.email} já existe")
        
        # Criar Value Objects
        email = Email(dto.email)
        telefone = Telefone(dto.telefone)
        
        # Criar Entity
        vendedor = Vendedor(
            nome=dto.nome,
            email=email,
            telefone=telefone,
            comissao_percentual=dto.comissao_percentual
        )
        
        # Persistir
        return self.repository.salvar(vendedor)
