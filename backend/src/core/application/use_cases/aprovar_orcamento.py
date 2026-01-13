from ..ports.repositories import IOrcamentoRepository
from ..dtos.orcamento_dtos import AprovarOrcamentoDTO
from ...domain.orcamentos.value_objects import OrcamentoId
from ...domain.orcamentos.exceptions import OrcamentoInvalidoException

class AprovarOrcamentoUseCase:
    
    def __init__(self, orcamento_repository: IOrcamentoRepository):
        self._repository = orcamento_repository
    
    async def execute(self, dto: AprovarOrcamentoDTO) -> None:
        orcamento = await self._repository.buscar_por_id(
            OrcamentoId(dto.orcamento_id)
        )
        
        if not orcamento:
            raise OrcamentoInvalidoException("Orçamento não encontrado")
        
        orcamento.aprovar(dto.aprovador)
        
        await self._repository.salvar(orcamento)
