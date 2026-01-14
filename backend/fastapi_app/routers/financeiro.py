"""Router com governança financeira por perfil."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from decimal import Decimal
from shared.domain.services.calculadora_financeira_governada import CalculadoraFinanceiraGovernada
from shared.infrastructure.auth.dependencies import get_current_user

router = APIRouter()


class CalculoFinanceiroRequest(BaseModel):
    custo_equipamentos: float
    qtd_modulos: int


@router.post("/api/financeiro/calcular/admin")
async def calcular_financeiro_admin(
    dados: CalculoFinanceiroRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    ADMIN ONLY - Retorna todos os dados financeiros.
    Requer role: ADMIN ou SUPERADMIN
    """
    if current_user.get("role") not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Acesso negado: apenas ADMIN")
    
    resultado = CalculadoraFinanceiraGovernada.calcular_preco_completo(
        Decimal(str(dados.custo_equipamentos)),
        dados.qtd_modulos
    )
    
    return {
        "perfil": "ADMIN",
        "dados_completos": resultado,
        "aviso": "Dados sensíveis - não compartilhar com vendedores"
    }


@router.post("/api/financeiro/calcular/vendedor")
async def calcular_financeiro_vendedor(
    dados: CalculoFinanceiroRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    VENDEDOR - Retorna APENAS preço final.
    SEM dados de custo, margem, comissão.
    """
    if current_user.get("role") not in ["VENDEDOR", "ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    resultado = CalculadoraFinanceiraGovernada.calcular_preco_vendedor(
        Decimal(str(dados.custo_equipamentos)),
        dados.qtd_modulos
    )
    
    return {
        "perfil": "VENDEDOR",
        "preco_final": resultado["preco_final"],
        "parcelas": resultado["parcelas_sugeridas"],
        "valor_parcela": resultado["valor_parcela"]
    }


@router.get("/api/financeiro/config")
async def obter_config_financeira(current_user: dict = Depends(get_current_user)):
    """
    ADMIN ONLY - Retorna configurações financeiras.
    """
    if current_user.get("role") not in ["ADMIN", "SUPERADMIN"]:
        raise HTTPException(status_code=403, detail="Acesso negado: apenas ADMIN")
    
    from shared.domain.config_financeira import CONFIG_FINANCEIRA
    
    return {
        "comissao_percentual": float(CONFIG_FINANCEIRA.COMISSAO_PERCENTUAL),
        "imposto_percentual": float(CONFIG_FINANCEIRA.IMPOSTO_PERCENTUAL),
        "margem_lucro_minima": float(CONFIG_FINANCEIRA.MARGEM_LUCRO_MINIMA),
        "custo_montagem_por_painel": float(CONFIG_FINANCEIRA.CUSTO_MONTAGEM_POR_PAINEL),
        "custo_operacional_fixo": float(CONFIG_FINANCEIRA.CUSTO_OPERACIONAL_FIXO),
        "arredondamento_multiplo": CONFIG_FINANCEIRA.ARREDONDAMENTO_MULTIPLO
    }
