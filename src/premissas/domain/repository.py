from abc import abstractmethod
from typing import List, Optional

from shared.domain.repository import Repository
from .entities import Premissa, CategoriaProduto, ConfiguracaoGlobal


class IPremissaRepository(Repository[Premissa]):
    @abstractmethod
    def find_by_item(self, item: str) -> Optional[Premissa]:
        pass
    
    @abstractmethod
    def find_by_categoria(self, categoria: CategoriaProduto) -> List[Premissa]:
        pass


class IConfiguracaoRepository(Repository[ConfiguracaoGlobal]):
    @abstractmethod
    def get_configuracao_atual(self) -> ConfiguracaoGlobal:
        pass
