from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from .value_objects import ItemId, KitId, CategoriaItem, Dinheiro, Quantidade, PotenciaWatts
from .events import DomainEvent, KitCriado, ItemAdicionado, ItemRemovido
from datetime import datetime

@dataclass(frozen=True)
class ItemKit:
    """Entity: Item de um kit solar (imutável)"""
    id: ItemId
    categoria: CategoriaItem
    nome: str
    marca: str
    potencia: Optional[PotenciaWatts]
    preco: Dinheiro
    quantidade: Quantidade
    descricao: str
    
    def calcular_subtotal(self) -> Dinheiro:
        return self.preco.multiplicar(self.quantidade.valor)
    
    def eh_painel_solar(self) -> bool:
        return self.categoria == CategoriaItem.PAINEL_SOLAR

@dataclass
class Kit:
    """Aggregate Root: Kit solar"""
    id: KitId
    nome: str
    itens: List[ItemKit] = field(default_factory=list)
    is_template: bool = False
    _events: List[DomainEvent] = field(default_factory=list, init=False, repr=False)
    
    def __post_init__(self):
        self._adicionar_evento(KitCriado(
            datetime.now(),
            self.id,
            self.nome,
            self.is_template
        ))
    
    def adicionar_item(self, item: ItemKit) -> None:
        self.itens.append(item)
        self._adicionar_evento(ItemAdicionado(
            datetime.now(),
            self.id,
            item.id,
            item.categoria.value
        ))
    
    def remover_item(self, item_id: ItemId) -> None:
        self.itens = [i for i in self.itens if i.id != item_id]
        self._adicionar_evento(ItemRemovido(
            datetime.now(),
            self.id,
            item_id
        ))
    
    def calcular_total(self) -> Dinheiro:
        total = Dinheiro(Decimal("0"))
        for item in self.itens:
            total = total.somar(item.calcular_subtotal())
        return total
    
    def obter_categorias_unicas(self) -> set:
        return {item.categoria for item in self.itens}
    
    def obter_eventos(self) -> List[DomainEvent]:
        return self._events.copy()
    
    def limpar_eventos(self) -> None:
        self._events.clear()
    
    def _adicionar_evento(self, evento: DomainEvent) -> None:
        self._events.append(evento)
