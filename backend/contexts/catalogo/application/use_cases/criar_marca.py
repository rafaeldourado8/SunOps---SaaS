"""
Use Case: Criar Marca
"""
from contexts.catalogo.domain.entities.marca import Marca
from contexts.catalogo.domain.repositories.marca_repository import MarcaRepository
from contexts.catalogo.application.dtos.marca_dto import CriarMarcaDTO


class CriarMarcaUseCase:
    """Use Case para criar marca"""
    
    def __init__(self, repository: MarcaRepository):
        self.repository = repository
    
    def execute(self, dto: CriarMarcaDTO) -> Marca:
        marca = Marca(nome=dto.nome)
        return self.repository.criar(marca)
