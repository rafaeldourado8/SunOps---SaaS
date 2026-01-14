"""Agente IA de Fallback - Totalmente governado pelas regras."""
from decimal import Decimal
from typing import Dict, List, Optional
from datetime import datetime


class AgenteIAFallback:
    """Agente IA que usa apenas regras do sistema."""
    
    TIMEOUT_ADMIN_MINUTOS = 15
    
    @staticmethod
    def pode_atuar(timestamp_solicitacao: datetime, tipo_solicitacao: str) -> bool:
        """Verifica se IA pode atuar."""
        tempo_decorrido = (datetime.now() - timestamp_solicitacao).total_seconds() / 60
        
        if tempo_decorrido < AgenteIAFallback.TIMEOUT_ADMIN_MINUTOS:
            return False
        
        if tipo_solicitacao not in ["PADRAO", "SIMPLES"]:
            return False
        
        return True
    
    @staticmethod
    def dimensionar_sistema(consumo_mensal: int, tipo_ligacao: str, cidade: str) -> Dict:
        """Dimensiona sistema usando motor de cálculo."""
        from contexts.orcamentos.application.dtos.orcamento_dto import InputOrcamento
        from contexts.orcamentos.application.use_cases.gerar_orcamento_automatico import (
            MotorOrcamentoAutomatico
        )
        
        input_data = InputOrcamento(
            cidade=cidade,
            consumo_mensal_kwh=consumo_mensal,
            tipo_ligacao=tipo_ligacao
        )
        
        motor = MotorOrcamentoAutomatico()
        output = motor.executar(input_data)
        
        return {
            "potencia_kwp": float(output.kit.potencia_instalada),
            "qtd_modulos": output.kit.qtd_modulos,
            "inversor": output.kit.inversor_nome,
            "geracao_mensal": float(output.geracao_mensal),
            "custo_estimado": float(output.financeiro.custo_total),
            "gerado_por": "IA_AUTOMATICA"
        }
    
    @staticmethod
    def selecionar_template(
        potencia_necessaria: Decimal,
        tipo: str,
        templates_disponiveis: List[Dict]
    ) -> Optional[Dict]:
        """Seleciona template mais próximo."""
        if not templates_disponiveis:
            return None
        
        templates_tipo = [t for t in templates_disponiveis if t["tipo"] == tipo]
        
        if not templates_tipo:
            templates_tipo = templates_disponiveis
        
        template_selecionado = min(
            templates_tipo,
            key=lambda t: abs(t["potencia_alvo_kwp"] - potencia_necessaria)
        )
        
        return {
            "template_id": template_selecionado["id"],
            "template_nome": template_selecionado["nome"],
            "potencia_kwp": template_selecionado["potencia_alvo_kwp"],
            "gerado_por": "IA_AUTOMATICA",
            "requer_revisao": True
        }
    
    @staticmethod
    def gerar_resposta(solicitacao: Dict, templates: List[Dict]) -> Dict:
        """Gera resposta completa para solicitação do campo."""
        dimensionamento = AgenteIAFallback.dimensionar_sistema(
            solicitacao["consumo_mensal"],
            solicitacao["tipo_ligacao"],
            solicitacao["cidade"]
        )
        
        template = AgenteIAFallback.selecionar_template(
            Decimal(str(dimensionamento["potencia_kwp"])),
            solicitacao.get("tipo", "RESIDENCIAL"),
            templates
        )
        
        return {
            "solicitacao_id": solicitacao["id"],
            "dimensionamento": dimensionamento,
            "template_sugerido": template,
            "gerado_por": "IA_AUTOMATICA",
            "requer_revisao_admin": True,
            "timestamp": datetime.now().isoformat(),
            "aviso": "Gerado por agente automático - Aguardando revisão"
        }
