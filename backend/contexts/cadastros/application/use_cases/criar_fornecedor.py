"""
Use Case: Criar Fornecedor
"""
from contexts.cadastros.domain.entities.fornecedor import Fornecedor
from contexts.cadastros.domain.repositories.fornecedor_repository import FornecedorRepository
from contexts.cadastros.application.dtos.fornecedor_dto import CriarFornecedorDTO
from shared.domain.value_objects.cnpj import CNPJ
from shared.domain.value_objects.email import Email
from shared.domain.value_objects.telefone import Telefone


class CriarFornecedorUseCase:
    """Use Case para criar fornecedor"""
    
    def __init__(self, repository: FornecedorRepository):
        self.repository = repository
    
    def execute(self, dto: CriarFornecedorDTO) -> Fornecedor:
        """Executa criação de fornecedor"""
        fornecedor = Fornecedor(
            nome=dto.nome,
            cnpj=CNPJ(dto.cnpj),
            email=Email(dto.email),
            telefone=Telefone(dto.telefone),
            endereco=dto.endereco
        )
        
        return self.repository.criar(fornecedor)
