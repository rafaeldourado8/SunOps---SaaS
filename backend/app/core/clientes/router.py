from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.users.models import User
# Importa as dependências de permissão
from app.core.auth.dependencies import get_current_user, get_current_gestor
from . import services, schema, models

router = APIRouter(tags=['Clientes'], prefix='/clientes')

@router.post(
    '/', 
    response_model=schema.ShowCliente, 
    status_code=status.HTTP_201_CREATED
)
async def create_cliente(
    cliente: schema.ClienteCreate,
    db: AsyncSession = Depends(get_db),
    # Permissão: Qualquer usuário logado pode criar um cliente
    current_user: User = Depends(get_current_user) 
):
    '''Cria um "Novo Cliente" no sistema'''
    
    # Verifica se o CPF/CNPJ já existe
    db_cliente = await services.get_cliente_by_documento(db, cliente.documento)
    if db_cliente:
        raise HTTPException(
            status_code=400, 
            detail="Um cliente com este documento (CPF/CNPJ) já existe."
        )
    return await services.create_new_cliente(db, cliente)


@router.get('/', response_model=List[schema.ShowCliente])
async def get_clientes_lista(
    q: Optional[str] = None, # Parâmetro de query para a busca
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
    Lista todos os clientes. 
    Se o parâmetro "q" for fornecido, filtra pelo nome.
    '''
    if q:
        # Se tem busca, usa o serviço de busca
        return await services.search_clientes(db, q)
    else:
        # Senão, lista todos
        return await services.get_all_clientes(db)


@router.get('/{cliente_id}', response_model=schema.ShowCliente)
async def get_cliente_detalhe(
    cliente_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''Busca um cliente específico pelo ID (para a tela "Ver detalhes")'''
    cliente = await services.get_cliente_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.delete(
    '/{cliente_id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_cliente(
    cliente_id: int,
    db: AsyncSession = Depends(get_db),
    # Permissão: Apenas Gestores podem deletar clientes
    gestor: User = Depends(get_current_gestor)
):
    '''Deleta um cliente (Apenas Gestores)'''
    cliente = await services.get_cliente_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Adicionar lógica de verificação (ex: não deletar se tiver projetos ativos)
    # if cliente.projetos:
    #     raise HTTPException(status_code=400, detail="Não é possível deletar cliente com projetos ativos.")

    await services.delete_cliente(db, cliente)
    return Response(status_code=status.HTTP_204_NO_CONTENT)