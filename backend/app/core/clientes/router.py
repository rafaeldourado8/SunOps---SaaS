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


# --- NOVO ENDPOINT DE ATUALIZAÇÃO (UPDATE) ---
@router.put(
    '/{cliente_id}', 
    response_model=schema.ShowCliente
)
async def update_cliente_endpoint(
    cliente_id: int,
    cliente_update: schema.ClienteUpdate,
    db: AsyncSession = Depends(get_db),
    # Permissão: Apenas Gestores podem alterar
    gestor: User = Depends(get_current_gestor)
):
    '''Atualiza um cliente específico pelo ID (Apenas Gestores)'''
    cliente = await services.get_cliente_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se o novo documento (se fornecido) já existe em OUTRO cliente
    if cliente_update.documento and cliente_update.documento != cliente.documento:
        db_cliente_doc = await services.get_cliente_by_documento(db, cliente_update.documento)
        if db_cliente_doc:
            raise HTTPException(
                status_code=400, 
                detail="Um cliente com este documento (CPF/CNPJ) já existe."
            )
            
    return await services.update_cliente(db, cliente, cliente_update)


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


# --- NOVO ENDPOINT DE DELEÇÃO EM MASSA (BULK DELETE) ---
@router.post(
    '/delete-bulk', 
    status_code=status.HTTP_200_OK
)
async def delete_clientes_bulk_endpoint(
    # Recebe um payload: {"cliente_ids": [1, 2, 3]}
    payload: dict[str, List[int]],
    db: AsyncSession = Depends(get_db),
    # Permissão: Apenas Gestores podem deletar
    gestor: User = Depends(get_current_gestor)
):
    '''Deleta múltiplos clientes (Apenas Gestores)'''
    
    cliente_ids = payload.get("cliente_ids", [])
    
    if not cliente_ids:
         raise HTTPException(
            status_code=400, 
            detail="Nenhum ID de cliente fornecido."
        )

    # (Você pode adicionar lógicas aqui, ex: não deletar clientes com projetos)

    deleted_count = await services.delete_clientes_bulk(db, cliente_ids)
    
    if deleted_count == 0:
         raise HTTPException(
            status_code=404, 
            detail="Nenhum cliente encontrado com os IDs fornecidos."
        )
        
    return {"detail": f"{deleted_count} cliente(s) deletado(s) com sucesso."}