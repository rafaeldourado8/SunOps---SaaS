"""Configurações financeiras - ADMIN ONLY."""
from decimal import Decimal
from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracaoFinanceira:
    """Premissas financeiras fixas do sistema."""
    
    # Percentuais
    COMISSAO_PERCENTUAL: Decimal = Decimal("0.05")  # 5%
    IMPOSTO_PERCENTUAL: Decimal = Decimal("0.06")   # 6%
    MARGEM_LUCRO_MINIMA: Decimal = Decimal("0.20")  # 20%
    
    # Custos fixos
    CUSTO_MONTAGEM_POR_PAINEL: Decimal = Decimal("70.00")
    CUSTO_OPERACIONAL_FIXO: Decimal = Decimal("500.00")
    
    # Arredondamento
    ARREDONDAMENTO_MULTIPLO: int = 100
    
    @property
    def percentual_total(self) -> Decimal:
        """Soma de todos os percentuais."""
        return self.COMISSAO_PERCENTUAL + self.IMPOSTO_PERCENTUAL + self.MARGEM_LUCRO_MINIMA


# Instância global (somente leitura)
CONFIG_FINANCEIRA = ConfiguracaoFinanceira()
