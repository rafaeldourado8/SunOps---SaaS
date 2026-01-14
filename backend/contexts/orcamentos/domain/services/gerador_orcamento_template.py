"""Serviço para gerar orçamento a partir de template."""
from decimal import Decimal
from typing import Dict, List, Tuple
from ..entities.template_kit import TemplateKit
from contexts.catalogo.domain.entities.cotacao import Cotacao, EstadoPreco


class GeradorOrcamentoTemplate:
    """Gera orçamento a partir de template com preços atualizados."""
    
    @staticmethod
    def validar_precos(cotacoes: Dict[str, Cotacao]) -> Tuple[bool, List[str]]:
        """
        Valida se todos os preços estão válidos.
        Retorna: (valido, lista_alertas)
        """
        alertas = []
        
        for produto_id, cotacao in cotacoes.items():
            if cotacao.estado == EstadoPreco.EXPIRED:
                alertas.append(
                    f"Produto {produto_id}: preço EXPIRADO (venceu há {abs(cotacao.dias_para_vencer)} dias)"
                )
            elif cotacao.estado == EstadoPreco.WARNING:
                alertas.append(
                    f"Produto {produto_id}: preço vence HOJE"
                )
        
        # Bloqueia se algum preço expirado
        tem_expirado = any(c.estado == EstadoPreco.EXPIRED for c in cotacoes.values())
        
        return (not tem_expirado, alertas)
    
    @staticmethod
    def calcular_custo_equipamentos(
        template: TemplateKit,
        cotacoes: Dict[str, Cotacao]
    ) -> Decimal:
        """Calcula custo total dos equipamentos com preços atuais."""
        total = Decimal("0")
        
        for item in template.itens:
            if item.produto_id not in cotacoes:
                raise ValueError(f"Cotação não encontrada para produto {item.produto_id}")
            
            cotacao = cotacoes[item.produto_id]
            
            if not cotacao.pode_usar_em_orcamento:
                raise ValueError(f"Preço expirado para produto {item.produto_id}")
            
            total += cotacao.preco * item.quantidade
        
        return total
    
    @staticmethod
    def gerar_orcamento(
        template: TemplateKit,
        cotacoes: Dict[str, Cotacao],
        margem: Decimal = Decimal("0.15"),
        impostos: Decimal = Decimal("0.165")
    ) -> Dict:
        """
        Gera orçamento completo a partir do template.
        
        Retorna:
        {
            "template_id": str,
            "custo_equipamentos": Decimal,
            "margem": Decimal,
            "impostos": Decimal,
            "custo_total": Decimal,
            "alertas": List[str],
            "itens": List[Dict]
        }
        """
        # Validar template
        erros = template.validar()
        if erros:
            raise ValueError(f"Template inválido: {', '.join(erros)}")
        
        # Validar preços
        precos_validos, alertas = GeradorOrcamentoTemplate.validar_precos(cotacoes)
        if not precos_validos:
            raise ValueError(f"Preços expirados: {', '.join(alertas)}")
        
        # Calcular custos
        custo_equipamentos = GeradorOrcamentoTemplate.calcular_custo_equipamentos(
            template,
            cotacoes
        )
        
        valor_margem = custo_equipamentos * margem
        valor_impostos = custo_equipamentos * impostos
        custo_total = custo_equipamentos + valor_margem + valor_impostos
        
        # Detalhar itens
        itens = []
        for item in template.itens:
            cotacao = cotacoes[item.produto_id]
            itens.append({
                "produto_id": item.produto_id,
                "categoria": item.categoria,
                "especificacao": item.especificacao,
                "quantidade": item.quantidade,
                "preco_unitario": cotacao.preco,
                "preco_total": cotacao.preco * item.quantidade,
                "estado_preco": cotacao.estado.value,
                "dias_para_vencer": cotacao.dias_para_vencer
            })
        
        return {
            "template_id": template.id,
            "template_nome": template.nome,
            "potencia_kwp": template.potencia_alvo_kwp,
            "tipo": template.tipo,
            "custo_equipamentos": custo_equipamentos,
            "margem": valor_margem,
            "impostos": valor_impostos,
            "custo_total": custo_total,
            "alertas": alertas,
            "itens": itens
        }
