from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from shared.domain.repository import Repository
from .entities import Proposta, StatusProposta


class IPropostaRepository(Repository[Proposta]):
    @abstractmethod
    def find_by_vendedor(self, vendedor_id: UUID) -> List[Proposta]:
        pass
    
    @abstractmethod
    def find_by_cliente(self, cliente_id: UUID) -> List[Proposta]:
        pass
    
    @abstractmethod
    def find_by_status(self, status: StatusProposta) -> List[Proposta]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass