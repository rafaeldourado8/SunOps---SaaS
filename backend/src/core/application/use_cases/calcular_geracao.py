from decimal import Decimal
from ..ports.repositories import IKitRepository
from ...domain.orcamentos.value_objects import KitId
from ...domain.orcamentos.services import CalculadoraGeracao
from ...domain.orcamentos.exceptions import KitInvalidoException

class CalcularGeracaoUseCase:
    
    def __init__(self, kit_repository: IKitRepository):
        self._repository = kit_repository
    
    async def execute(self, kit_id: str) -> dict:
        kit = await self._repository.buscar_por_id(KitId(kit_id))
        
        if not kit:
            raise KitInvalidoException("Kit não encontrado")
        
        kwp = CalculadoraGeracao.calcular_kwp_total(kit.itens)
        kwh_mes = CalculadoraGeracao.calcular_kwh_mes(kwp)
        
        return {
            "kwp_total": float(kwp),
            "kwh_mes": float(kwh_mes),
            "valor_total": float(kit.calcular_total().valor)
        }
