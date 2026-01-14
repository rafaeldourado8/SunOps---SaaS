"""Router para geração de orçamentos."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from contexts.orcamentos.application.dtos.orcamento_dto import InputOrcamento
from contexts.orcamentos.application.use_cases.gerar_orcamento_automatico import MotorOrcamentoAutomatico

router = APIRouter()


class SolicitacaoOrcamento(BaseModel):
    """Dados para solicitar orçamento."""
    nome_cliente: str
    cidade: str
    conta_energia: float  # R$/mês
    tipo_ligacao: str = "MONOFASICA"
    tipo_telhado: str = "CERAMICO"
    forma_pagamento: str = "A_VISTA"
    classe_tarifaria: str = "B1"


@router.post("/api/orcamentos/gerar")
async def gerar_orcamento(dados: SolicitacaoOrcamento):
    """Gera orçamento automático."""
    
    # Estimar consumo baseado na conta
    tarifa_media = Decimal("0.80")
    consumo_kwh = int(dados.conta_energia / float(tarifa_media))
    
    # Gerar orçamento
    input_data = InputOrcamento(
        cidade=dados.cidade,
        consumo_mensal_kwh=consumo_kwh,
        tipo_ligacao=dados.tipo_ligacao,
        tipo_telhado=dados.tipo_telhado,
        forma_pagamento=dados.forma_pagamento,
        classe_tarifaria=dados.classe_tarifaria
    )
    
    motor = MotorOrcamentoAutomatico()
    output = motor.executar(input_data)
    
    # Formatar resposta
    return {
        "cliente": {
            "nome": dados.nome_cliente,
            "cidade": dados.cidade,
            "conta_atual": dados.conta_energia,
            "consumo_estimado": consumo_kwh
        },
        "dimensionamento": {
            "consumo_medio": float(output.consumo_medio),
            "consumo_compensavel": float(output.consumo_compensavel),
            "potencia_necessaria": float(output.potencia_necessaria)
        },
        "kit": {
            "modulos": {
                "quantidade": output.kit.qtd_modulos,
                "modelo": output.kit.modulo_nome,
                "potencia_unitaria": float(output.kit.potencia_modulo)
            },
            "inversor": {
                "modelo": output.kit.inversor_nome,
                "potencia": float(output.kit.potencia_inversor)
            },
            "potencia_instalada": float(output.kit.potencia_instalada),
            "dc_ac_ratio": float(output.kit.dc_ac_ratio),
            "dc_ac_valido": output.kit.dc_ac_valido
        },
        "geracao": {
            "mensal_kwh": float(output.geracao_mensal),
            "anual_kwh": float(output.geracao_anual),
            "hsp": float(output.hsp_utilizado),
            "fator_perdas": float(output.fator_perdas)
        },
        "financeiro": {
            "custo_equipamentos": float(output.financeiro.custo_equipamentos),
            "custo_estrutura": float(output.financeiro.custo_estrutura),
            "custo_mao_obra": float(output.financeiro.custo_mao_obra),
            "impostos": float(output.financeiro.impostos),
            "margem": float(output.financeiro.margem),
            "investimento_total": float(output.financeiro.custo_total),
            "economia_mensal": float(output.financeiro.economia_mensal),
            "economia_anual": float(output.financeiro.economia_anual),
            "payback_anos": float(output.financeiro.payback_anos)
        },
        "projecao_25_anos": {
            "economia_total": float(output.financeiro.economia_anual * 25),
            "lucro_liquido": float(output.financeiro.economia_anual * 25 - output.financeiro.custo_total)
        },
        "alertas": output.alertas,
        "performance": {
            "tempo_processamento_ms": output.tempo_processamento_ms
        }
    }
