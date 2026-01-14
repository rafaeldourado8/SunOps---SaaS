"""
Repository Interface para Marca (Port)
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from contexts.catalogo.domain.entities.marca import Marca


class MarcaRepository(ABC):
    """Interface do repositório"""
    
    @abstractmethod
    def criar(self, marca: Marca) -> Marca:
        pass
    
    @abstractmethod
    def buscar_por_id(self, marca_id: int) -> Optional[Marca]:
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Marca]:
        pass
    
    @abstractmethod
    def atualizar(self, marca: Marca) -> Marca:
        pass
    
    @abstractmethod
    def deletar(self, marca_id: int) -> bool:
        pass
