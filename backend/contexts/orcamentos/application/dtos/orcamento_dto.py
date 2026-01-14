"""DTOs para entrada e saída do motor de orçamento."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List


@dataclass
class InputOrcamento:
    """Entrada mínima para gerar orçamento automático."""
    
    # Obrigatórios
    cidade: str
    consumo_mensal_kwh: int  # Pode ser média ou lista de 12 meses
    tipo_ligacao: str  # MONOFASICA, BIFASICA, TRIFASICA
    
    # Opcionais com defaults
    tipo_telhado: str = "CERAMICO"
    forma_pagamento: str = "A_VISTA"  # A_VISTA, FINANCIADO
    classe_tarifaria: str = "B1"
    
    # Financiamento (se aplicável)
    taxa_juros_mensal: Optional[Decimal] = None
    num_parcelas: Optional[int] = None
    
    # Override manual (opcional)
    potencia_modulo_override: Optional[Decimal] = None
    qtd_modulos_override: Optional[int] = None
    inversor_id_override: Optional[str] = None


@dataclass
class SugestaoKit:
    """Sugestão automática de kit."""
    
    modulo_id: str
    modulo_nome: str
    potencia_modulo: Decimal
    qtd_modulos: int
    
    inversor_id: str
    inversor_nome: str
    potencia_inversor: Decimal
    
    potencia_instalada: Decimal
    dc_ac_ratio: Decimal
    dc_ac_valido: bool


@dataclass
class CalculosFinanceiros:
    """Resultados dos cálculos financeiros."""
    
    custo_equipamentos: Decimal
    custo_estrutura: Decimal
    custo_mao_obra: Decimal
    impostos: Decimal
    margem: Decimal
    custo_total: Decimal
    
    economia_mensal: Decimal
    economia_anual: Decimal
    payback_anos: Decimal
    
    # Financiamento (se aplicável)
    parcela_mensal: Optional[Decimal] = None
    delta_mensal: Optional[Decimal] = None
    mes_break_even: Optional[int] = None


@dataclass
class OutputOrcamento:
    """Saída completa do orçamento automático."""
    
    # Dimensionamento
    consumo_medio: Decimal
    consumo_compensavel: Decimal
    potencia_necessaria: Decimal
    
    # Kit sugerido
    kit: SugestaoKit
    
    # Geração
    geracao_mensal: Decimal
    geracao_anual: Decimal
    hsp_utilizado: Decimal
    fator_perdas: Decimal
    
    # Financeiro
    financeiro: CalculosFinanceiros
    
    # Alertas
    alertas: List[str]
    
    # Tempo de processamento
    tempo_processamento_ms: int
