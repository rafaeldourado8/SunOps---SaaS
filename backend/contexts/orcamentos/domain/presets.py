"""Presets e configurações padrão do sistema."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict


@dataclass(frozen=True)
class PresetTelhado:
    """Preset de tipo de telhado."""
    CERAMICO = "CERAMICO"
    METALICO = "METALICO"
    FIBROCIMENTO = "FIBROCIMENTO"
    
    tipo: str
    custo_estrutura_por_modulo: Decimal
    
    def __post_init__(self):
        validos = [self.CERAMICO, self.METALICO, self.FIBROCIMENTO]
        if self.tipo not in validos:
            raise ValueError(f"Tipo deve ser: {validos}")


@dataclass(frozen=True)
class ConfiguracaoSistema:
    """Configurações padrão do sistema."""
    
    # Perdas
    FATOR_PERDAS_RESIDENCIAL = Decimal("0.80")
    FATOR_PERDAS_COMERCIAL = Decimal("0.82")
    
    # Degradação
    TAXA_DEGRADACAO_ANUAL = Decimal("0.006")  # 0.6%
    
    # DC/AC Ratio
    DC_AC_MIN = Decimal("1.10")
    DC_AC_MAX = Decimal("1.30")
    
    # Distância e altura padrão
    DISTANCIA_PADRAO = 10  # metros
    ALTURA_PADRAO = 6  # metros
    
    # Margem e impostos
    MARGEM_MINIMA = Decimal("0.15")  # 15%
    IMPOSTOS = Decimal("0.165")  # 16.5% (PIS/COFINS/ICMS simplificado)
    
    # Mão de obra (% do equipamento)
    MAO_OBRA_PERCENTUAL = Decimal("0.20")  # 20%


# Cache de HSP por cidade (dados CRESESB)
HSP_POR_CIDADE: Dict[str, Decimal] = {
    "São Paulo": Decimal("4.42"),
    "Rio de Janeiro": Decimal("4.59"),
    "Belo Horizonte": Decimal("4.69"),
    "Brasília": Decimal("5.26"),
    "Salvador": Decimal("5.08"),
    "Fortaleza": Decimal("5.45"),
    "Recife": Decimal("5.28"),
    "Curitiba": Decimal("4.21"),
    "Porto Alegre": Decimal("4.29"),
    "Manaus": Decimal("4.54"),
    "Goiânia": Decimal("5.13"),
    "Campinas": Decimal("4.45"),
    "Florianópolis": Decimal("4.06"),
    "Vitória": Decimal("4.72"),
    "Natal": Decimal("5.61"),
}


# Tarifa média por classe (configurável por tenant)
TARIFA_MEDIA_POR_CLASSE: Dict[str, Decimal] = {
    "B1": Decimal("0.80"),  # Residencial
    "B2": Decimal("0.75"),  # Rural
    "B3": Decimal("0.85"),  # Demais classes
    "A4": Decimal("0.65"),  # Comercial/Industrial
}


# Presets de telhado
PRESETS_TELHADO = {
    PresetTelhado.CERAMICO: PresetTelhado(
        PresetTelhado.CERAMICO,
        Decimal("80.00")  # R$ por módulo
    ),
    PresetTelhado.METALICO: PresetTelhado(
        PresetTelhado.METALICO,
        Decimal("60.00")
    ),
    PresetTelhado.FIBROCIMENTO: PresetTelhado(
        PresetTelhado.FIBROCIMENTO,
        Decimal("70.00")
    ),
}
