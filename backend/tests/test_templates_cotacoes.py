"""Testes para sistema de templates e cotações."""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from contexts.catalogo.domain.entities.cotacao import Cotacao, EstadoPreco, HistoricoPreco
from contexts.orcamentos.domain.entities.template_kit import (
    TemplateKit, ItemTemplate, RegrasTemplate
)
from contexts.orcamentos.domain.services.gerador_orcamento_template import (
    GeradorOrcamentoTemplate
)
from contexts.catalogo.domain.services.analisador_mercado import AnalisadorMercado


def test_cotacao_valida():
    """Teste: cotação válida (4 dias úteis)."""
    cotacao = Cotacao(
        id="cot-1",
        produto_id="prod-1",
        fornecedor_id="forn-1",
        preco=Decimal("1200.00"),
        data_cotacao=datetime.now(),
        validade_dias_uteis=4
    )
    
    assert cotacao.estado == EstadoPreco.VALID
    assert cotacao.pode_usar_em_orcamento is True
    assert cotacao.dias_para_vencer >= 3


def test_cotacao_warning():
    """Teste: cotação em warning (1 dia para vencer)."""
    tres_dias_atras = datetime.now() - timedelta(days=3)
    cotacao = Cotacao(
        id="cot-2",
        produto_id="prod-2",
        fornecedor_id="forn-1",
        preco=Decimal("3000.00"),
        data_cotacao=tres_dias_atras,
        validade_dias_uteis=4
    )
    
    assert cotacao.estado == EstadoPreco.WARNING
    assert cotacao.pode_usar_em_orcamento is True


def test_cotacao_expirada():
    """Teste: cotação expirada."""
    cinco_dias_atras = datetime.now() - timedelta(days=7)
    cotacao = Cotacao(
        id="cot-3",
        produto_id="prod-3",
        fornecedor_id="forn-1",
        preco=Decimal("500.00"),
        data_cotacao=cinco_dias_atras,
        validade_dias_uteis=4
    )
    
    assert cotacao.estado == EstadoPreco.EXPIRED
    assert cotacao.pode_usar_em_orcamento is False


def test_historico_preco_variacao():
    """Teste: cálculo de variação percentual."""
    hist = HistoricoPreco(
        timestamp=datetime.now(),
        fornecedor_id="forn-1",
        produto_id="prod-1",
        sku="SKU-123",
        preco=Decimal("1100.00"),
        preco_anterior=Decimal("1000.00")
    )
    
    assert hist.variacao_percentual == Decimal("10.00")
    assert hist.tendencia == "ALTA"


def test_template_kit_validacao():
    """Teste: validação de template."""
    template = TemplateKit(
        id="tmpl-1",
        nome="Kit 5kWp Residencial",
        potencia_alvo_kwp=Decimal("5.0"),
        tipo="RESIDENCIAL"
    )
    
    template.adicionar_item(ItemTemplate(
        produto_id="mod-550w",
        categoria="MODULO",
        quantidade=9,
        especificacao="550W Monocristalino"
    ))
    
    template.adicionar_item(ItemTemplate(
        produto_id="inv-5kw",
        categoria="INVERSOR",
        quantidade=1,
        especificacao="5kW String"
    ))
    
    erros = template.validar()
    assert len(erros) == 0
    assert template.quantidade_modulos == 9
    assert template.tem_inversor is True


def test_gerador_orcamento_template():
    """Teste: gerar orçamento a partir de template."""
    template = TemplateKit(
        id="tmpl-1",
        nome="Kit 5kWp",
        potencia_alvo_kwp=Decimal("5.0"),
        tipo="RESIDENCIAL"
    )
    
    template.adicionar_item(ItemTemplate(
        produto_id="mod-1",
        categoria="MODULO",
        quantidade=9,
        especificacao="550W"
    ))
    
    template.adicionar_item(ItemTemplate(
        produto_id="inv-1",
        categoria="INVERSOR",
        quantidade=1,
        especificacao="5kW"
    ))
    
    cotacoes = {
        "mod-1": Cotacao(
            id="cot-1",
            produto_id="mod-1",
            fornecedor_id="forn-1",
            preco=Decimal("1200.00"),
            data_cotacao=datetime.now()
        ),
        "inv-1": Cotacao(
            id="cot-2",
            produto_id="inv-1",
            fornecedor_id="forn-1",
            preco=Decimal("3000.00"),
            data_cotacao=datetime.now()
        )
    }
    
    orcamento = GeradorOrcamentoTemplate.gerar_orcamento(template, cotacoes)
    
    assert orcamento["template_id"] == "tmpl-1"
    assert orcamento["custo_equipamentos"] == Decimal("13800.00")  # 9*1200 + 3000
    assert orcamento["custo_total"] > orcamento["custo_equipamentos"]
    assert len(orcamento["itens"]) == 2


def test_gerador_bloqueia_preco_expirado():
    """Teste: bloqueia orçamento com preço expirado."""
    template = TemplateKit(
        id="tmpl-1",
        nome="Kit 5kWp",
        potencia_alvo_kwp=Decimal("5.0"),
        tipo="RESIDENCIAL"
    )
    
    template.adicionar_item(ItemTemplate(
        produto_id="mod-1",
        categoria="MODULO",
        quantidade=9,
        especificacao="550W"
    ))
    
    template.adicionar_item(ItemTemplate(
        produto_id="inv-1",
        categoria="INVERSOR",
        quantidade=1,
        especificacao="5kW"
    ))
    
    cotacoes = {
        "mod-1": Cotacao(
            id="cot-1",
            produto_id="mod-1",
            fornecedor_id="forn-1",
            preco=Decimal("1200.00"),
            data_cotacao=datetime.now() - timedelta(days=10),
            validade_dias_uteis=4
        ),
        "inv-1": Cotacao(
            id="cot-2",
            produto_id="inv-1",
            fornecedor_id="forn-1",
            preco=Decimal("3000.00"),
            data_cotacao=datetime.now() - timedelta(days=10),
            validade_dias_uteis=4
        )
    }
    
    with pytest.raises(ValueError):
        GeradorOrcamentoTemplate.gerar_orcamento(template, cotacoes)


def test_analisador_mercado_preco_medio():
    """Teste: cálculo de preço médio."""
    historico = [
        HistoricoPreco(
            timestamp=datetime.now(),
            fornecedor_id="f1",
            produto_id="p1",
            sku="SKU1",
            preco=Decimal("1000"),
            preco_anterior=Decimal("950")
        ),
        HistoricoPreco(
            timestamp=datetime.now(),
            fornecedor_id="f2",
            produto_id="p1",
            sku="SKU1",
            preco=Decimal("1100"),
            preco_anterior=Decimal("1000")
        )
    ]
    
    preco_medio = AnalisadorMercado.calcular_preco_medio(historico)
    assert preco_medio == Decimal("1050")


def test_analisador_mercado_melhor_fornecedor():
    """Teste: sugestão de melhor fornecedor."""
    cotacoes = {
        "forn-1": Decimal("1200"),
        "forn-2": Decimal("1100"),
        "forn-3": Decimal("1250")
    }
    
    melhor = AnalisadorMercado.sugerir_melhor_fornecedor(cotacoes)
    assert melhor == "forn-2"


def test_analisador_mercado_volatilidade():
    """Teste: detecção de volatilidade."""
    historico = [
        HistoricoPreco(
            timestamp=datetime.now() - timedelta(days=2),
            fornecedor_id="f1",
            produto_id="p1",
            sku="SKU1",
            preco=Decimal("1000"),
            preco_anterior=Decimal("850")  # +17.6%
        ),
        HistoricoPreco(
            timestamp=datetime.now() - timedelta(days=1),
            fornecedor_id="f1",
            produto_id="p1",
            sku="SKU1",
            preco=Decimal("950"),
            preco_anterior=Decimal("1000")  # -5%
        )
    ]
    
    volatil = AnalisadorMercado.detectar_volatilidade(historico)
    assert volatil is True
