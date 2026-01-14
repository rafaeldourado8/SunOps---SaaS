"""
Repository Interface (Port) para Cliente

SOLID: 
- Interface Segregation: Interface específica para Cliente
- Dependency Inversion: Use Cases dependem desta abstração
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

import sys
sys.path.append('../../..')
from contexts.cadastros.domain.entities import Cliente


class ClienteRepository(ABC):
    """
    Port (Interface) para persistência de Cliente.
    
    Adapters (implementações) podem ser:
    - ClienteRepositoryPostgreSQL
    - ClienteRepositoryMongoDB
    - ClienteRepositoryInMemory (para testes)
    """
    
    @abstractmethod
    def salvar(self, cliente: Cliente) -> Cliente:
        """
        Salva ou atualiza cliente.
        Complexidade: 1
        """
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: UUID) -> Optional[Cliente]:
        """
        Busca cliente por ID.
        Complexidade: 1
        """
        pass
    
    @abstractmethod
    def buscar_por_documento(self, documento: str) -> Optional[Cliente]:
        """
        Busca cliente por CPF/CNPJ.
        Complexidade: 1
        """
        pass
    
    @abstractmethod
    def listar_todos(self, apenas_ativos: bool = True) -> List[Cliente]:
        """
        Lista todos os clientes.
        Complexidade: 1
        """
        pass
    
    @abstractmethod
    def deletar(self, id: UUID) -> bool:
        """
        Deleta cliente por ID.
        Complexidade: 1
        """
        pass
