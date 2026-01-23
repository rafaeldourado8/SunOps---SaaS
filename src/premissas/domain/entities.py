from dataclasses import dataclass
from enum import Enum
from typing import Optional

from shared.domain.entity import Entity
from shared.domain.value_objects import Money


class CategoriaProduto(Enum):
    KIT = "KIT"
    SERVICO = "SERVICO"
    CUSTO = "CUSTO"


@dataclass
class Premissa(Entity):
    categoria: CategoriaProduto = CategoriaProduto.KIT
    item: str = ""
    custo_unitario: Money = None
    margem_lucro: float = 0.18
    comissao: float = 0.05
    imposto: float = 0.0
    
    def calcular_preco_venda(self) -> Money:
        custo = self.custo_unitario.value
        preco = custo / (1 - self.margem_lucro - self.comissao - self.imposto)
        return Money(round(preco, 2))


@dataclass
class ConfiguracaoGlobal(Entity):
    montagem_por_painel: Money = Money(60.0)
    custo_projeto: Money = Money(400.0)
    margem_lucro_padrao: float = 0.18
    comissao_padrao: float = 0.05
    imposto_padrao: float = 0.0
