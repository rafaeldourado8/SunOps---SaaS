from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.users.models import User
from app.core.auth.dependencies import get_current_user, get_current_gestor # Ajuste permissões conforme necessário
from . import services, schema, models

router = APIRouter(tags=['Equipamentos'], prefix='/equipamentos')

# --- Distribuidor Endpoints ---

@router.post('/distribuidores/', response_model=schema.ShowDistribuidor, status_code=status.HTTP_201_CREATED, summary="Cria um novo distribuidor")
async def create_distribuidor_endpoint(
    distribuidor: schema.DistribuidorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_gestor) # Apenas gestor pode criar
):
    existing = await services.get_distribuidor_by_nome(db, distribuidor.nome)
    if existing:
        raise HTTPException(status_code=400, detail="Distribuidor com este nome já existe.")
    return await services.create_distribuidor(db, distribuidor)

@router.get('/distribuidores/', response_model=List[schema.ShowDistribuidor], summary="Lista todos os distribuidores")
async def list_distribuidores_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) # Qualquer usuário logado pode ver
):
    return await services.get_all_distribuidores(db)

# --- Categoria Endpoints ---

@router.post('/categorias/', response_model=schema.ShowCategoriaEquipamento, status_code=status.HTTP_201_CREATED, summary="Cria uma nova categoria")
async def create_categoria_endpoint(
    categoria: schema.CategoriaEquipamentoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_gestor)
):
    # Adicionar validação se nome já existe, se necessário
    return await services.create_categoria(db, categoria)

@router.get('/categorias/', response_model=List[schema.ShowCategoriaEquipamento], summary="Lista todas as categorias")
async def list_categorias_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await services.get_all_categorias(db)

# --- Equipamento Endpoints ---

@router.post('/', response_model=schema.ShowEquipamento, status_code=status.HTTP_201_CREATED, summary="Cria um novo equipamento")
async def create_equipamento_endpoint(
    equipamento: schema.EquipamentoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_gestor)
):
    # Adicionar validação se nome_modelo já existe, se necessário
    return await services.create_equipamento(db, equipamento)

@router.get('/', response_model=List[schema.ShowEquipamento], summary="Lista todos os equipamentos")
async def list_equipamentos_endpoint(
    categoria_id: Optional[int] = None, # Filtro opcional
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista equipamentos, opcionalmente filtrando por categoria_id."""
    return await services.get_all_equipamentos(db, categoria_id=categoria_id)


# --- CatalogoItem Endpoints ---

@router.post('/catalogo/', response_model=schema.ShowCatalogoItem, status_code=status.HTTP_201_CREATED, summary="Cria um item de catálogo (associa equipamento a distribuidor com preço)")
async def create_catalogo_item_endpoint(
    item: schema.CatalogoItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_gestor)
):
    # Adicionar validações (ex: se equipamento e distribuidor existem)
    return await services.create_catalogo_item(db, item)

@router.get('/catalogo/', response_model=List[schema.ShowCatalogoItem], summary="Lista itens do catálogo")
async def list_catalogo_itens_endpoint(
    equipamento_id: Optional[int] = None,
    distribuidor_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista itens do catálogo, com filtros opcionais."""
    return await services.get_all_catalogo_itens(db, equipamento_id=equipamento_id, distribuidor_id=distribuidor_id)

# --- Kit Endpoints ---

@router.post('/kits/', response_model=schema.ShowKit, status_code=status.HTTP_201_CREATED, summary="Cria um novo kit")
async def create_kit_endpoint(
    kit: schema.KitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_gestor)
):
    # Validações: checar se distribuidor existe, se itens existem, etc.
    return await services.create_kit(db, kit)

@router.get('/kits/', response_model=List[schema.ShowKit], summary="Lista todos os kits")
async def list_kits_endpoint(
    distribuidor_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista kits, opcionalmente filtrando por distribuidor."""
    return await services.get_all_kits(db, distribuidor_id=distribuidor_id)

# Adicionar endpoints GET por ID, PUT, DELETE conforme necessário...