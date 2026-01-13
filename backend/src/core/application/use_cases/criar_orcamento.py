import uuid
from ..ports.repositories import IKitRepository, IOrcamentoRepository
from ..dtos.orcamento_dtos import CriarOrcamentoDTO
from ...domain.orcamentos.aggregates import Orcamento
from ...domain.orcamentos.value_objects import OrcamentoId, KitId
from ...domain.orcamentos.services import ValidadorKit
from ...domain.orcamentos.exceptions import KitInvalidoException

class CriarOrcamentoUseCase:
    
    def __init__(
        self, 
        kit_repository: IKitRepository,
        orcamento_repository: IOrcamentoRepository
    ):
        self._kit_repo = kit_repository
        self._orcamento_repo = orcamento_repository
    
    async def execute(self, dto: CriarOrcamentoDTO) -> str:
        kit = await self._kit_repo.buscar_por_id(KitId(dto.kit_id))
        
        if not kit:
            raise KitInvalidoException("Kit não encontrado")
        
        if not ValidadorKit.validar(kit):
            raise KitInvalidoException("Kit deve ter no mínimo 2 categorias")
        
        orcamento_id = OrcamentoId(str(uuid.uuid4()))
        
        orcamento = Orcamento(
            id=orcamento_id,
            kit=kit,
            cliente_nome=dto.cliente_nome,
            cliente_contato=dto.cliente_contato,
            validade_dias=dto.validade_dias
        )
        
        await self._orcamento_repo.salvar(orcamento)
        
        return orcamento_id
