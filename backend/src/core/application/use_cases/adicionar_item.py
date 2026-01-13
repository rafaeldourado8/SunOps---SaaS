import uuid
from ..ports.repositories import IKitRepository
from ..dtos.orcamento_dtos import AdicionarItemDTO
from ...domain.orcamentos.entities import ItemKit
from ...domain.orcamentos.value_objects import (
    ItemId, KitId, CategoriaItem, Dinheiro, Quantidade, PotenciaWatts
)
from ...domain.orcamentos.exceptions import KitInvalidoException

class AdicionarItemUseCase:
    
    def __init__(self, kit_repository: IKitRepository):
        self._repository = kit_repository
    
    async def execute(self, dto: AdicionarItemDTO) -> str:
        kit = await self._repository.buscar_por_id(KitId(dto.kit_id))
        
        if not kit:
            raise KitInvalidoException("Kit não encontrado")
        
        item_id = ItemId(str(uuid.uuid4()))
        potencia = PotenciaWatts(dto.potencia_watts) if dto.potencia_watts else None
        
        item = ItemKit(
            id=item_id,
            categoria=CategoriaItem(dto.categoria),
            nome=dto.nome,
            marca=dto.marca,
            potencia=potencia,
            preco=Dinheiro(dto.preco),
            quantidade=Quantidade(dto.quantidade),
            descricao=dto.descricao
        )
        
        kit.adicionar_item(item)
        await self._repository.salvar(kit)
        
        return item_id
