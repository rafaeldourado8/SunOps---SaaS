from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from shared.infrastructure.auth.dependencies import get_current_user
from contexts.cadastros.application.use_cases.criar_fornecedor import CriarFornecedorUseCase
from contexts.cadastros.application.dtos.fornecedor_dto import CriarFornecedorDTO
from contexts.cadastros.infrastructure.repositories.fornecedor_repository_postgres import FornecedorRepositoryPostgreSQL

router = APIRouter()


class FornecedorRequest(BaseModel):
    nome: str
    cnpj: str
    email: str
    telefone: str
    endereco: str | None = None


class FornecedorResponse(BaseModel):
    id: str
    nome: str
    cnpj: str
    email: str
    telefone: str
    endereco: str | None
    ativo: bool


@router.post("", response_model=FornecedorResponse, status_code=201)
async def criar_fornecedor(
    request: FornecedorRequest,
    current_user: dict = Depends(get_current_user)
):
    repository = FornecedorRepositoryPostgreSQL()
    use_case = CriarFornecedorUseCase(repository)
    
    dto = CriarFornecedorDTO(
        nome=request.nome,
        cnpj=request.cnpj,
        email=request.email,
        telefone=request.telefone,
        endereco=request.endereco
    )
    
    fornecedor = use_case.execute(dto)
    
    return {
        "id": str(fornecedor.id),
        "nome": fornecedor.nome,
        "cnpj": fornecedor.cnpj.numero,
        "email": fornecedor.email.endereco,
        "telefone": fornecedor.telefone.numero,
        "endereco": fornecedor.endereco,
        "ativo": fornecedor.ativo
    }


@router.get("", response_model=List[FornecedorResponse])
async def listar_fornecedores(current_user: dict = Depends(get_current_user)):
    repository = FornecedorRepositoryPostgreSQL()
    fornecedores = repository.listar_todos()
    
    return [
        {
            "id": str(f.id),
            "nome": f.nome,
            "cnpj": f.cnpj.numero,
            "email": f.email.endereco,
            "telefone": f.telefone.numero,
            "endereco": f.endereco,
            "ativo": f.ativo
        }
        for f in fornecedores
    ]
