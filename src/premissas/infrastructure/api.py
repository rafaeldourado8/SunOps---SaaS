from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from typing import List

from shared.infrastructure.database import get_db
from premissas.application.use_cases import CriarPremissaUseCase, CriarPremissaDTO, ObterPrecoPorItemUseCase, AtualizarConfiguracaoUseCase
from premissas.infrastructure.repository import SQLAlchemyPremissaRepository, SQLAlchemyConfiguracaoRepository

router = APIRouter(prefix="/premissas", tags=["premissas"])


class PremissaRequest(BaseModel):
    categoria: str
    item: str
    custo_unitario: float
    margem_lucro: float = 0.18
    comissao: float = 0.05
    imposto: float = 0.0


class ConfiguracaoRequest(BaseModel):
    montagem_por_painel: float
    custo_projeto: float
    margem_lucro: float
    comissao: float
    imposto: float


class CalcularPrecoRequest(BaseModel):
    item: str
    quantidade: int


@router.post("/")
async def criar_premissa(request: PremissaRequest, db: Session = Depends(get_db)):
    repository = SQLAlchemyPremissaRepository(db)
    use_case = CriarPremissaUseCase(repository)
    
    dto = CriarPremissaDTO(
        categoria=request.categoria,
        item=request.item,
        custo_unitario=request.custo_unitario,
        margem_lucro=request.margem_lucro,
        comissao=request.comissao,
        imposto=request.imposto
    )
    
    premissa = use_case.execute(dto)
    preco_venda = premissa.calcular_preco_venda()
    
    return {
        "id": premissa.id,
        "item": premissa.item,
        "custo_unitario": premissa.custo_unitario.value,
        "preco_venda": preco_venda.value
    }


@router.get("/")
async def listar_premissas(db: Session = Depends(get_db)):
    repository = SQLAlchemyPremissaRepository(db)
    premissas = repository.find_all()
    
    return [
        {
            "id": p.id,
            "categoria": p.categoria.value,
            "item": p.item,
            "custo_unitario": p.custo_unitario.value,
            "preco_venda": p.calcular_preco_venda().value
        }
        for p in premissas
    ]


@router.post("/calcular-preco")
async def calcular_preco(request: CalcularPrecoRequest, db: Session = Depends(get_db)):
    premissa_repo = SQLAlchemyPremissaRepository(db)
    config_repo = SQLAlchemyConfiguracaoRepository(db)
    use_case = ObterPrecoPorItemUseCase(premissa_repo, config_repo)
    
    resultado = use_case.execute(request.item, request.quantidade)
    return resultado


@router.put("/configuracao")
async def atualizar_configuracao(request: ConfiguracaoRequest, db: Session = Depends(get_db)):
    repository = SQLAlchemyConfiguracaoRepository(db)
    use_case = AtualizarConfiguracaoUseCase(repository)
    
    config = use_case.execute(
        montagem_por_painel=request.montagem_por_painel,
        custo_projeto=request.custo_projeto,
        margem_lucro=request.margem_lucro,
        comissao=request.comissao,
        imposto=request.imposto
    )
    
    return {
        "montagem_por_painel": config.montagem_por_painel.value,
        "custo_projeto": config.custo_projeto.value,
        "margem_lucro": config.margem_lucro_padrao,
        "comissao": config.comissao_padrao,
        "imposto": config.imposto_padrao
    }


@router.get("/configuracao")
async def obter_configuracao(db: Session = Depends(get_db)):
    repository = SQLAlchemyConfiguracaoRepository(db)
    config = repository.get_configuracao_atual()
    
    return {
        "montagem_por_painel": config.montagem_por_painel.value,
        "custo_projeto": config.custo_projeto.value,
        "margem_lucro": config.margem_lucro_padrao,
        "comissao": config.comissao_padrao,
        "imposto": config.imposto_padrao
    }
