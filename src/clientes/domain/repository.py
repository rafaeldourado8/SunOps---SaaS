from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from shared.domain.repository import Repository
from .entities import Cliente, StatusCliente


class IClienteRepository(Repository[Cliente]):
    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def find_by_cnpj(self, cnpj: str) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def find_by_vendedor(self, vendedor_id: UUID) -> List[Cliente]:
        pass
    
    @abstractmethod
    def find_by_status(self, status: StatusCliente) -> List[Cliente]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass