import uuid
from ..ports.repositories import IKitRepository
from ..dtos.orcamento_dtos import CriarKitDTO
from ...domain.orcamentos.entities import Kit
from ...domain.orcamentos.value_objects import KitId

class CriarKitUseCase:
    
    def __init__(self, kit_repository: IKitRepository):
        self._repository = kit_repository
    
    async def execute(self, dto: CriarKitDTO) -> str:
        kit_id = KitId(str(uuid.uuid4()))
        
        kit = Kit(
            id=kit_id,
            nome=dto.nome,
            is_template=dto.is_template
        )
        
        await self._repository.salvar(kit)
        
        return kit_id
