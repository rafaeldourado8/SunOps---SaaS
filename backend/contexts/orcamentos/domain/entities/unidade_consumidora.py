"""Entity Unidade Consumidora."""
from dataclasses import dataclass
from decimal import Decimal
from ..value_objects.dados_uc import (
    TipoLigacao, Tensao, ClasseTarifaria, Tarifa, 
    Localizacao, HistoricoConsumo
)


@dataclass
class UnidadeConsumidora:
    """Unidade Consumidora do cliente."""
    
    id: str
    cliente_id: str
    historico_consumo: HistoricoConsumo
    tipo_ligacao: TipoLigacao
    tensao: Tensao
    classe_tarifaria: ClasseTarifaria
    tarifa: Tarifa
    localizacao: Localizacao
    
    @property
    def consumo_medio(self) -> Decimal:
        """Consumo médio mensal em kWh."""
        return self.historico_consumo.media_mensal
    
    @property
    def geracao_necessaria(self) -> Decimal:
        """Geração necessária descontando custo de disponibilidade."""
        custo_disp = self.tipo_ligacao.custo_disponibilidade
        return self.consumo_medio - Decimal(custo_disp)
