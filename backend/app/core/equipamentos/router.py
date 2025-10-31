from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import redis.asyncio as aioredis # Importar aioredis

from app.db import get_db
from app.core.auth.dependencies import get_current_user
from app.core.users.models import User
from . import schema, services

# Importar a nova dependência de cache
from app.cache import get_redis_client

router = APIRouter(prefix="/equipamentos", tags=["Equipamentos"])

# --- Endpoint ATUALIZADO ---
@router.get(
    "/", 
    response_model=List[schema.ShowEquipamento],
    summary="Lista Equipamentos (Módulos, Inversores, etc.)"
)
async def get_equipamentos(
    categoria_id: Optional[int] = Query(None, description="Filtrar por ID da categoria"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """
    Lista todos os equipamentos técnicos (Módulos, Inversores) 
    cadastrados no banco (baseado no script 'seed_equipamentos').
    
    Use o parâmetro `categoria_id` para filtrar (ex: Módulos ou Inversores).
    """
    return await services.get_equipamentos(db=db, categoria_id=categoria_id)

# --- Endpoint MANTIDO ---
@router.get(
    "/categorias/", 
    response_model=List[schema.ShowCategoria],
    summary="Lista todas as Categorias de Equipamentos"
)
async def get_categorias(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await services.get_all_categorias(db=db)

# --- Endpoints Opcionais (Mantidos do seu projeto original) ---

@router.get(
    "/distribuidores/", 
    response_model=List[schema.ShowDistribuidor],
    summary="Lista todos os Distribuidores"
)
async def get_distribuidores(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await services.get_all_distribuidores(db=db)


# --- Endpoint /catalogo/ (MODIFICADO COM CACHE) ---
@router.get(
    "/catalogo/", 
    response_model=List[schema.ShowCatalogoItem],
    summary="Lista todos os Itens de Catálogo (SKUs com preço)"
)
async def get_catalogo_itens(
    db: AsyncSession = Depends(get_db),
    # Adicionar a dependência do Redis
    redis_client: aioredis.Redis = Depends(get_redis_client),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém a lista completa de itens do catálogo.
    Esta consulta é otimizada com cache-aside usando Redis.
    """
    # O serviço agora retorna List[dict], que o FastAPI validará
    # contra o response_model.
    return await services.get_all_catalogo_itens(db=db, redis_client=redis_client)


@router.get(
    "/kits/", 
    response_model=List[schema.ShowKit],
    summary="Lista todos os Kits"
)
async def get_kits(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await services.get_all_kits(db=db)