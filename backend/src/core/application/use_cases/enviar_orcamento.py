from ..ports.repositories import IOrcamentoRepository
from ...domain.orcamentos.value_objects import OrcamentoId
from ...domain.orcamentos.exceptions import OrcamentoInvalidoException

class EnviarOrcamentoUseCase:
    
    def __init__(self, orcamento_repository: IOrcamentoRepository):
        self._repository = orcamento_repository
    
    async def execute(self, orcamento_id: str) -> None:
        orcamento = await self._repository.buscar_por_id(
            OrcamentoId(orcamento_id)
        )
        
        if not orcamento:
            raise OrcamentoInvalidoException("Orçamento não encontrado")
        
        orcamento.enviar()
        
        await self._repository.salvar(orcamento)
        
        # Eventos serão processados por handlers
        # Ex: EnviarEmailHandler, EnviarWhatsAppHandler
