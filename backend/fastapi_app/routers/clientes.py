from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from shared.infrastructure.auth.dependencies import get_current_user
from contexts.cadastros.application.use_cases.criar_cliente import CriarClienteUseCase, CriarClienteDTO
from contexts.cadastros.infrastructure.repositories.cliente_repository_postgres import ClienteRepositoryPostgreSQL

router = APIRouter()


class ClienteRequest(BaseModel):
    nome: str
    tipo_documento: str
    numero_documento: str
    email: str
    telefone: str


class ClienteResponse(BaseModel):
    id: int
    nome: str
    tipo_documento: str
    numero_documento: str
    email: str
    telefone: str


@router.post("", response_model=ClienteResponse, status_code=201)
async def criar_cliente(
    request: ClienteRequest,
    current_user: dict = Depends(get_current_user)
):
    repository = ClienteRepositoryPostgreSQL()
    use_case = CriarClienteUseCase(repository)
    
    dto = CriarClienteDTO(
        nome=request.nome,
        tipo_documento=request.tipo_documento,
        numero_documento=request.numero_documento,
        email=request.email,
        telefone=request.telefone
    )
    
    cliente = use_case.execute(dto)
    
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "tipo_documento": cliente.tipo_documento,
        "numero_documento": cliente.numero_documento,
        "email": cliente.email,
        "telefone": cliente.telefone
    }


@router.get("", response_model=List[ClienteResponse])
async def listar_clientes(current_user: dict = Depends(get_current_user)):
    repository = ClienteRepositoryPostgreSQL()
    clientes = repository.listar_todos()
    
    return [
        {
            "id": c.id,
            "nome": c.nome,
            "tipo_documento": c.tipo_documento,
            "numero_documento": c.numero_documento,
            "email": c.email,
            "telefone": c.telefone
        }
        for c in clientes
    ]
