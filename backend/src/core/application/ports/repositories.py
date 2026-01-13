from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.orcamentos.entities import Kit
from ...domain.orcamentos.aggregates import Orcamento
from ...domain.orcamentos.value_objects import KitId, OrcamentoId

class IKitRepository(ABC):
    
    @abstractmethod
    async def salvar(self, kit: Kit) -> None:
        pass
    
    @abstractmethod
    async def buscar_por_id(self, kit_id: KitId) -> Optional[Kit]:
        pass
    
    @abstractmethod
    async def listar_templates(self) -> List[Kit]:
        pass

class IOrcamentoRepository(ABC):
    
    @abstractmethod
    async def salvar(self, orcamento: Orcamento) -> None:
        pass
    
    @abstractmethod
    async def buscar_por_id(self, orcamento_id: OrcamentoId) -> Optional[Orcamento]:
        pass
    
    @abstractmethod
    async def listar_expirados(self) -> List[Orcamento]:
        pass
