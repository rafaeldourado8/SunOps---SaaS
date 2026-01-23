from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from shared.domain.repository import Repository
from .entities import Contrato, StatusContrato
from .template import Template


class IContratoRepository(Repository[Contrato]):
    @abstractmethod
    def find_by_proposta(self, proposta_id: UUID) -> Optional[Contrato]:
        pass
    
    @abstractmethod
    def find_by_cliente(self, cliente_id: UUID) -> List[Contrato]:
        pass
    
    @abstractmethod
    def find_by_status(self, status: StatusContrato) -> List[Contrato]:
        pass


class ITemplateRepository(Repository[Template]):
    @abstractmethod
    def find_by_vendedor(self, vendedor_id: UUID) -> List[Template]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass