"""
Repository Interface (Port) para Vendedor

SOLID: Interface Segregation + Dependency Inversion
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

import sys
sys.path.append('../../..')
from contexts.cadastros.domain.entities import Vendedor


class VendedorRepository(ABC):
    """Port (Interface) para persistência de Vendedor."""
    
    @abstractmethod
    def salvar(self, vendedor: Vendedor) -> Vendedor:
        """Salva ou atualiza vendedor. Complexidade: 1"""
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[Vendedor]:
        """Busca vendedor por ID. Complexidade: 1"""
        pass
    
    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Vendedor]:
        """Busca vendedor por email. Complexidade: 1"""
        pass
    
    @abstractmethod
    def listar_todos(self, apenas_ativos: bool = True) -> List[Vendedor]:
        """Lista todos os vendedores. Complexidade: 1"""
        pass
    
    @abstractmethod
    def deletar(self, id: UUID) -> bool:
        """Deleta vendedor por ID. Complexidade: 1"""
        pass
