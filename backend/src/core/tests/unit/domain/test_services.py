import pytest
from decimal import Decimal
from src.core.domain.orcamentos.services import CalculadoraGeracao, ValidadorKit

class TestCalculadoraGeracao:
    
    def test_calcular_kwp_total(self, kit_valido):
        kwp = CalculadoraGeracao.calcular_kwp_total(kit_valido.itens)
        # 10 painéis * 550W = 5500W = 5.5kWp
        assert kwp == Decimal("5.5")
    
    def test_calcular_kwh_mes(self):
        kwp = Decimal("5.5")
        kwh_mes = CalculadoraGeracao.calcular_kwh_mes(kwp)
        # 5.5 * 0.7 * 126 = 485.1
        assert kwh_mes == Decimal("485.1")
    
    def test_calcular_kwh_mes_com_kit_completo(self, kit_valido):
        kwp = CalculadoraGeracao.calcular_kwp_total(kit_valido.itens)
        kwh_mes = CalculadoraGeracao.calcular_kwh_mes(kwp)
        assert kwh_mes > 0

class TestValidadorKit:
    
    def test_kit_valido_com_duas_categorias(self, kit_valido):
        assert ValidadorKit.validar(kit_valido) is True
    
    def test_kit_invalido_com_uma_categoria(self, item_painel):
        from src.core.domain.orcamentos.entities import Kit
        from src.core.domain.orcamentos.value_objects import KitId
        import uuid
        
        kit = Kit(
            id=KitId(str(uuid.uuid4())),
            nome="Kit Incompleto"
        )
        kit.adicionar_item(item_painel)
        
        assert ValidadorKit.validar(kit) is False
