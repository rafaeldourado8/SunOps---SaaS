from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ....core.application.use_cases.criar_orcamento import CriarOrcamentoUseCase
from ....core.application.use_cases.aprovar_orcamento import AprovarOrcamentoUseCase
from ....core.application.use_cases.enviar_orcamento import EnviarOrcamentoUseCase
from ....core.application.dtos.orcamento_dtos import (
    CriarOrcamentoDTO, AprovarOrcamentoDTO
)
from ..dependencies import get_db, get_kit_repository, get_orcamento_repository

router = APIRouter(prefix="/orcamentos", tags=["orcamentos"])

class CriarOrcamentoRequest(BaseModel):
    kit_id: str
    cliente_nome: str
    cliente_contato: str
    validade_dias: int = 3

class AprovarOrcamentoRequest(BaseModel):
    aprovador: str

class OrcamentoResponse(BaseModel):
    id: str
    cliente_nome: str
    status: str

@router.post("/", response_model=OrcamentoResponse)
async def criar_orcamento(
    request: CriarOrcamentoRequest,
    session: AsyncSession = Depends(get_db)
):
    kit_repo = get_kit_repository(session)
    orc_repo = get_orcamento_repository(session)
    use_case = CriarOrcamentoUseCase(kit_repo, orc_repo)
    
    dto = CriarOrcamentoDTO(
        kit_id=request.kit_id,
        cliente_nome=request.cliente_nome,
        cliente_contato=request.cliente_contato,
        validade_dias=request.validade_dias
    )
    
    try:
        orcamento_id = await use_case.execute(dto)
        return OrcamentoResponse(
            id=orcamento_id,
            cliente_nome=request.cliente_nome,
            status="rascunho"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{orcamento_id}/aprovar")
async def aprovar_orcamento(
    orcamento_id: str,
    request: AprovarOrcamentoRequest,
    session: AsyncSession = Depends(get_db)
):
    repository = get_orcamento_repository(session)
    use_case = AprovarOrcamentoUseCase(repository)
    
    dto = AprovarOrcamentoDTO(
        orcamento_id=orcamento_id,
        aprovador=request.aprovador
    )
    
    try:
        await use_case.execute(dto)
        return {"message": "Orçamento aprovado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{orcamento_id}/enviar")
async def enviar_orcamento(
    orcamento_id: str,
    session: AsyncSession = Depends(get_db)
):
    repository = get_orcamento_repository(session)
    use_case = EnviarOrcamentoUseCase(repository)
    
    try:
        await use_case.execute(orcamento_id)
        return {"message": "Orçamento enviado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{orcamento_id}")
async def buscar_orcamento(
    orcamento_id: str,
    session: AsyncSession = Depends(get_db)
):
    repository = get_orcamento_repository(session)
    orcamento = await repository.buscar_por_id(orcamento_id)
    
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orçamento não encontrado")
    
    return {
        "id": str(orcamento.id),
        "cliente_nome": orcamento.cliente_nome,
        "status": orcamento.status.value,
        "valor_total": float(orcamento.calcular_total().valor),
        "aprovado_por": orcamento.aprovado_por
    }
