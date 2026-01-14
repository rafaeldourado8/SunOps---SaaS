"""Seletor automático de kit (módulo + inversor)."""
from decimal import Decimal
from typing import Optional, Tuple
from ..presets import ConfiguracaoSistema


class SeletorAutomaticoKit:
    """Seleciona automaticamente módulo e inversor compatíveis."""
    
    @staticmethod
    def selecionar_modulo_padrao() -> Tuple[str, Decimal]:
        """
        Retorna módulo padrão do sistema.
        TODO: Buscar do banco de dados o módulo mais vendido/disponível.
        """
        return ("modulo-550w", Decimal("0.550"))
    
    @staticmethod
    def calcular_quantidade_modulos(
        potencia_necessaria: Decimal,
        potencia_modulo: Decimal
    ) -> int:
        """Calcula quantidade de módulos (arredonda para cima)."""
        import math
        qtd = potencia_necessaria / potencia_modulo
        return math.ceil(qtd)
    
    @staticmethod
    def calcular_potencia_instalada(
        qtd_modulos: int,
        potencia_modulo: Decimal
    ) -> Decimal:
        """Calcula potência instalada real."""
        return Decimal(qtd_modulos) * potencia_modulo
    
    @staticmethod
    def selecionar_inversor_compativel(
        potencia_instalada: Decimal
    ) -> Tuple[str, Decimal]:
        """
        Seleciona inversor compatível com DC/AC ratio ideal.
        TODO: Buscar do banco de dados inversores compatíveis.
        
        Lógica:
        - DC/AC ideal: 1.10 a 1.30
        - Potência inversor = potencia_instalada / 1.20 (médio)
        """
        potencia_inversor = potencia_instalada / Decimal("1.20")
        
        # Arredondar para potências comerciais
        potencias_comerciais = [
            Decimal("1.0"), Decimal("1.5"), Decimal("2.0"),
            Decimal("3.0"), Decimal("4.0"), Decimal("5.0"),
            Decimal("6.0"), Decimal("8.0"), Decimal("10.0")
        ]
        
        # Seleciona a potência comercial mais próxima
        potencia_selecionada = min(
            potencias_comerciais,
            key=lambda x: abs(x - potencia_inversor)
        )
        
        return (f"inversor-{potencia_selecionada}kw", potencia_selecionada)
    
    @staticmethod
    def validar_dc_ac_ratio(
        potencia_instalada: Decimal,
        potencia_inversor: Decimal
    ) -> Tuple[Decimal, bool]:
        """
        Valida DC/AC ratio.
        Retorna: (ratio, valido)
        """
        ratio = potencia_instalada / potencia_inversor
        valido = (
            ConfiguracaoSistema.DC_AC_MIN <= ratio <= ConfiguracaoSistema.DC_AC_MAX
        )
        return (ratio, valido)
    
    @staticmethod
    def ajustar_kit_se_necessario(
        qtd_modulos: int,
        potencia_modulo: Decimal,
        potencia_inversor: Decimal
    ) -> Tuple[int, str]:
        """
        Ajusta kit se DC/AC inválido.
        Retorna: (nova_qtd_modulos, inversor_id)
        """
        potencia_instalada = Decimal(qtd_modulos) * potencia_modulo
        ratio, valido = SeletorAutomaticoKit.validar_dc_ac_ratio(
            potencia_instalada,
            potencia_inversor
        )
        
        if valido:
            return (qtd_modulos, f"inversor-{potencia_inversor}kw")
        
        # Ajusta para DC/AC = 1.20 (ideal)
        nova_potencia_instalada = potencia_inversor * Decimal("1.20")
        nova_qtd = int(nova_potencia_instalada / potencia_modulo)
        
        return (nova_qtd, f"inversor-{potencia_inversor}kw")
