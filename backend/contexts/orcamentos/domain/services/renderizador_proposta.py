"""Serviço de renderização de propostas."""
from typing import Dict
import re
from decimal import Decimal


class RenderizadorProposta:
    """Renderiza template com dados do orçamento."""
    
    @staticmethod
    def formatar_valor(valor, tipo: str) -> str:
        """Formata valor conforme tipo."""
        if tipo == 'MOEDA':
            return f"R$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        elif tipo == 'NUMERO':
            return f"{float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        elif tipo == 'PERCENTUAL':
            return f"{float(valor):.1%}"
        else:
            return str(valor)
    
    @staticmethod
    def injetar_dados(template_html: str, mapeamento: Dict, dados_orcamento: Dict) -> str:
        """Injeta dados do orçamento no template."""
        html = template_html
        
        # Para cada binding no mapeamento
        for label, campo_info in mapeamento.get('bindings', {}).items():
            campo_nome = campo_info.get('campo')
            campo_tipo = campo_info.get('tipo', 'TEXTO')
            
            # Busca valor nos dados
            valor = dados_orcamento.get(campo_nome, '')
            
            # Formata valor
            valor_formatado = RenderizadorProposta.formatar_valor(valor, campo_tipo)
            
            # Substitui no HTML
            pattern = r'\{\{' + re.escape(label) + r'\}\}'
            html = re.sub(pattern, valor_formatado, html)
        
        return html
    
    @staticmethod
    def gerar_proposta(
        template_html: str,
        mapeamento: Dict,
        dados_orcamento: Dict
    ) -> str:
        """Gera proposta completa."""
        return RenderizadorProposta.injetar_dados(
            template_html,
            mapeamento,
            dados_orcamento
        )
