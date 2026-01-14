from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from shared.infrastructure.auth.dependencies import get_current_user
from contexts.catalogo.application.use_cases.criar_marca import CriarMarcaUseCase
from contexts.catalogo.application.dtos.marca_dto import CriarMarcaDTO
from contexts.catalogo.infrastructure.repositories.marca_repository_postgres import MarcaRepositoryPostgreSQL

router = APIRouter()


class MarcaRequest(BaseModel):
    nome: str


class MarcaResponse(BaseModel):
    id: str
    nome: str
    ativo: bool


@router.post("", response_model=MarcaResponse, status_code=201)
async def criar_marca(
    request: MarcaRequest,
    current_user: dict = Depends(get_current_user)
):
    repository = MarcaRepositoryPostgreSQL()
    use_case = CriarMarcaUseCase(repository)
    
    dto = CriarMarcaDTO(nome=request.nome)
    marca = use_case.execute(dto)
    
    return {
        "id": str(marca.id),
        "nome": marca.nome,
        "ativo": marca.ativo
    }


@router.get("", response_model=List[MarcaResponse])
async def listar_marcas(current_user: dict = Depends(get_current_user)):
    repository = MarcaRepositoryPostgreSQL()
    marcas = repository.listar_todos()
    
    return [
        {
            "id": str(m.id),
            "nome": m.nome,
            "ativo": m.ativo
        }
        for m in marcas
    ]
