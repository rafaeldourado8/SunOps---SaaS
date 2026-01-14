"""Sistema de rastreamento de preços com validade."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum


class EstadoPreco(Enum):
    """Estados do preço."""
    VALID = "VALID"
    WARNING = "WARNING"
    EXPIRED = "EXPIRED"


@dataclass
class Cotacao:
    """Cotação de preço de produto."""
    
    id: str
    produto_id: str
    fornecedor_id: str
    preco: Decimal
    data_cotacao: datetime
    validade_dias_uteis: int = 4
    
    def _calcular_data_vencimento(self) -> datetime:
        """Calcula data de vencimento considerando apenas dias úteis."""
        data = self.data_cotacao
        dias_adicionados = 0
        
        while dias_adicionados < self.validade_dias_uteis:
            data += timedelta(days=1)
            # Segunda a sexta (0-4)
            if data.weekday() < 5:
                dias_adicionados += 1
        
        return data
    
    @property
    def data_vencimento(self) -> datetime:
        """Data de vencimento da cotação."""
        return self._calcular_data_vencimento()
    
    @property
    def dias_para_vencer(self) -> int:
        """Dias úteis restantes até vencimento."""
        hoje = datetime.now()
        if hoje >= self.data_vencimento:
            return 0
        
        dias = 0
        data = hoje
        while data < self.data_vencimento:
            if data.weekday() < 5:
                dias += 1
            data += timedelta(days=1)
        
        return dias
    
    @property
    def estado(self) -> EstadoPreco:
        """Estado atual do preço."""
        dias = self.dias_para_vencer
        
        if dias == 0:
            return EstadoPreco.EXPIRED
        elif dias == 1:
            return EstadoPreco.WARNING
        else:
            return EstadoPreco.VALID
    
    @property
    def pode_usar_em_orcamento(self) -> bool:
        """Preço pode ser usado em novos orçamentos."""
        return self.estado != EstadoPreco.EXPIRED


@dataclass
class HistoricoPreco:
    """Histórico de variação de preço."""
    
    timestamp: datetime
    fornecedor_id: str
    produto_id: str
    sku: str
    preco: Decimal
    preco_anterior: Decimal
    
    @property
    def variacao_percentual(self) -> Decimal:
        """Variação percentual em relação ao preço anterior."""
        if self.preco_anterior == 0:
            return Decimal("0")
        
        return ((self.preco - self.preco_anterior) / self.preco_anterior) * Decimal("100")
    
    @property
    def tendencia(self) -> str:
        """Tendência: ALTA, QUEDA, ESTAVEL."""
        variacao = self.variacao_percentual
        
        if variacao > Decimal("5"):
            return "ALTA"
        elif variacao < Decimal("-5"):
            return "QUEDA"
        else:
            return "ESTAVEL"
