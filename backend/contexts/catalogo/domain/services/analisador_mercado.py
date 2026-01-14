"""Inteligência de mercado - análise de preços."""
from decimal import Decimal
from typing import List, Dict
from datetime import datetime, timedelta
from ..entities.cotacao import HistoricoPreco


class AnalisadorMercado:
    """Analisa tendências de mercado sem IA."""
    
    @staticmethod
    def calcular_preco_medio(historico: List[HistoricoPreco]) -> Decimal:
        """Calcula preço médio de mercado."""
        if not historico:
            return Decimal("0")
        
        total = sum(h.preco for h in historico)
        return total / len(historico)
    
    @staticmethod
    def identificar_tendencia(historico: List[HistoricoPreco]) -> str:
        """Identifica tendência: ALTA, QUEDA, ESTAVEL."""
        if len(historico) < 2:
            return "ESTAVEL"
        
        trinta_dias_atras = datetime.now() - timedelta(days=30)
        historico_recente = [
            h for h in historico 
            if h.timestamp >= trinta_dias_atras
        ]
        
        if not historico_recente:
            return "ESTAVEL"
        
        variacoes = [h.variacao_percentual for h in historico_recente]
        media_variacao = sum(variacoes) / len(variacoes)
        
        if media_variacao > Decimal("5"):
            return "ALTA"
        elif media_variacao < Decimal("-5"):
            return "QUEDA"
        else:
            return "ESTAVEL"
    
    @staticmethod
    def sugerir_melhor_fornecedor(cotacoes: Dict[str, Decimal]) -> str:
        """Sugere fornecedor com melhor preço."""
        if not cotacoes:
            return None
        return min(cotacoes, key=cotacoes.get)
    
    @staticmethod
    def detectar_volatilidade(historico: List[HistoricoPreco]) -> bool:
        """Detecta volatilidade alta (variações > 10% em 7 dias)."""
        if len(historico) < 2:
            return False
        
        sete_dias_atras = datetime.now() - timedelta(days=7)
        historico_recente = [
            h for h in historico 
            if h.timestamp >= sete_dias_atras
        ]
        
        if not historico_recente:
            return False
        
        return any(
            abs(h.variacao_percentual) > Decimal("10") 
            for h in historico_recente
        )
    
    @staticmethod
    def gerar_relatorio(
        produto_id: str,
        historico: List[HistoricoPreco],
        cotacoes_atuais: Dict[str, Decimal]
    ) -> Dict:
        """Gera relatório de inteligência de mercado."""
        return {
            "produto_id": produto_id,
            "preco_medio": AnalisadorMercado.calcular_preco_medio(historico),
            "tendencia": AnalisadorMercado.identificar_tendencia(historico),
            "melhor_fornecedor": AnalisadorMercado.sugerir_melhor_fornecedor(cotacoes_atuais),
            "volatilidade_alta": AnalisadorMercado.detectar_volatilidade(historico),
            "num_cotacoes": len(historico),
            "num_fornecedores": len(cotacoes_atuais)
        }
