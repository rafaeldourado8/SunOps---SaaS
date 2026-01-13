import pytest
from decimal import Decimal
from datetime import datetime
import uuid

from src.core.domain.orcamentos.value_objects import (
    ItemId, KitId, OrcamentoId, CategoriaItem, 
    Dinheiro, Quantidade, PotenciaWatts
)
from src.core.domain.orcamentos.entities import ItemKit, Kit
from src.core.domain.orcamentos.aggregates import Orcamento

@pytest.fixture
def item_painel():
    return ItemKit(
        id=ItemId(str(uuid.uuid4())),
        categoria=CategoriaItem.PAINEL_SOLAR,
        nome="Painel 550W",
        marca="Canadian Solar",
        potencia=PotenciaWatts(550),
        preco=Dinheiro(Decimal("800.00")),
        quantidade=Quantidade(10),
        descricao="Painel monocristalino"
    )

@pytest.fixture
def item_inversor():
    return ItemKit(
        id=ItemId(str(uuid.uuid4())),
        categoria=CategoriaItem.INVERSOR,
        nome="Inversor 5kW",
        marca="Growatt",
        potencia=None,
        preco=Dinheiro(Decimal("3500.00")),
        quantidade=Quantidade(1),
        descricao="Inversor on-grid"
    )

@pytest.fixture
def kit_valido(item_painel, item_inversor):
    kit = Kit(
        id=KitId(str(uuid.uuid4())),
        nome="Kit Residencial 5kW",
        is_template=False
    )
    kit.adicionar_item(item_painel)
    kit.adicionar_item(item_inversor)
    return kit

@pytest.fixture
def orcamento_valido(kit_valido):
    return Orcamento(
        id=OrcamentoId(str(uuid.uuid4())),
        kit=kit_valido,
        cliente_nome="João Silva",
        cliente_contato="11999999999"
    )
