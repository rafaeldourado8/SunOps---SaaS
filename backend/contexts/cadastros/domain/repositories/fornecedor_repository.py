"""
Repository Interface para Fornecedor (Port)
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from contexts.cadastros.domain.entities.fornecedor import Fornecedor


class FornecedorRepository(ABC):
    """Interface do repositório (Dependency Inversion Principle)"""
    
    @abstractmethod
    def criar(self, fornecedor: Fornecedor) -> Fornecedor:
        pass
    
    @abstractmethod
    def buscar_por_id(self, fornecedor_id: int) -> Optional[Fornecedor]:
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Fornecedor]:
        pass
    
    @abstractmethod
    def atualizar(self, fornecedor: Fornecedor) -> Fornecedor:
        pass
    
    @abstractmethod
    def deletar(self, fornecedor_id: int) -> bool:
        pass
