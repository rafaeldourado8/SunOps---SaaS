from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

from ....core.application.use_cases.criar_kit import CriarKitUseCase
from ....core.application.use_cases.adicionar_item import AdicionarItemUseCase
from ....core.application.use_cases.calcular_geracao import CalcularGeracaoUseCase
from ....core.application.dtos.orcamento_dtos import CriarKitDTO, AdicionarItemDTO
from ..dependencies import get_db, get_kit_repository

router = APIRouter(prefix="/kits", tags=["kits"])

# Schemas Pydantic
class CriarKitRequest(BaseModel):
    nome: str
    is_template: bool = False

class AdicionarItemRequest(BaseModel):
    categoria: str
    nome: str
    marca: str
    potencia_watts: Optional[int] = None
    preco: Decimal
    quantidade: int
    descricao: str = ""

class KitResponse(BaseModel):
    id: str
    nome: str
    is_template: bool

class GeracaoResponse(BaseModel):
    kwp_total: float
    kwh_mes: float
    valor_total: float

@router.post("/", response_model=KitResponse)
async def criar_kit(
    request: CriarKitRequest,
    session: AsyncSession = Depends(get_db)
):
    repository = get_kit_repository(session)
    use_case = CriarKitUseCase(repository)
    
    dto = CriarKitDTO(nome=request.nome, is_template=request.is_template)
    kit_id = await use_case.execute(dto)
    
    return KitResponse(id=kit_id, nome=request.nome, is_template=request.is_template)

@router.post("/{kit_id}/itens")
async def adicionar_item(
    kit_id: str,
    request: AdicionarItemRequest,
    session: AsyncSession = Depends(get_db)
):
    repository = get_kit_repository(session)
    use_case = AdicionarItemUseCase(repository)
    
    dto = AdicionarItemDTO(
        kit_id=kit_id,
        categoria=request.categoria,
        nome=request.nome,
        marca=request.marca,
        potencia_watts=request.potencia_watts,
        preco=request.preco,
        quantidade=request.quantidade,
        descricao=request.descricao
    )
    
    try:
        item_id = await use_case.execute(dto)
        return {"item_id": item_id, "message": "Item adicionado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{kit_id}/geracao", response_model=GeracaoResponse)
async def calcular_geracao(
    kit_id: str,
    session: AsyncSession = Depends(get_db)
):
    repository = get_kit_repository(session)
    use_case = CalcularGeracaoUseCase(repository)
    
    try:
        resultado = await use_case.execute(kit_id)
        return GeracaoResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/templates")
async def listar_templates(session: AsyncSession = Depends(get_db)):
    repository = get_kit_repository(session)
    kits = await repository.listar_templates()
    
    return [
        {"id": str(kit.id), "nome": kit.nome, "total_itens": len(kit.itens)}
        for kit in kits
    ]
