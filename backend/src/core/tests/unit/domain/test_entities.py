import pytest
from decimal import Decimal
from src.core.domain.orcamentos.value_objects import CategoriaItem

class TestItemKit:
    
    def test_calcular_subtotal(self, item_painel):
        subtotal = item_painel.calcular_subtotal()
        assert subtotal.valor == Decimal("8000.00")  # 800 * 10
    
    def test_eh_painel_solar(self, item_painel, item_inversor):
        assert item_painel.eh_painel_solar() is True
        assert item_inversor.eh_painel_solar() is False

class TestKit:
    
    def test_adicionar_item(self, kit_valido, item_painel):
        inicial = len(kit_valido.itens)
        kit_valido.adicionar_item(item_painel)
        assert len(kit_valido.itens) == inicial + 1
    
    def test_remover_item(self, kit_valido):
        item_id = kit_valido.itens[0].id
        kit_valido.remover_item(item_id)
        assert len(kit_valido.itens) == 1
    
    def test_calcular_total(self, kit_valido):
        total = kit_valido.calcular_total()
        # 10 painéis * 800 + 1 inversor * 3500 = 11500
        assert total.valor == Decimal("11500.00")
    
    def test_obter_categorias_unicas(self, kit_valido):
        categorias = kit_valido.obter_categorias_unicas()
        assert len(categorias) == 2
        assert CategoriaItem.PAINEL_SOLAR in categorias
        assert CategoriaItem.INVERSOR in categorias
    
    def test_eventos_sao_gerados(self, kit_valido):
        eventos = kit_valido.obter_eventos()
        assert len(eventos) > 0
