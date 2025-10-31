import json
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from typing import List, Optional
from . import models, schema

# --- Definições do Cache ---
CATALOGO_CACHE_KEY = "catalogo_itens:all"
CATALOGO_CACHE_TTL_SECONDS = 3600  # Cache por 1 hora

# --- Equipamentos (Itens ANEEL) ---

async def get_equipamentos(db: AsyncSession, categoria_id: Optional[int] = None) -> List[models.Equipamento]:
    """
    Busca equipamentos técnicos (Módulos, Inversores).
    Filtra por categoria_id se fornecido.
    """
    query = (
        select(models.Equipamento)
        .options(joinedload(models.Equipamento.categoria))
        .order_by(models.Equipamento.fabricante, models.Equipamento.nome_modelo)
    )
    
    if categoria_id:
        query = query.where(models.Equipamento.categoria_id == categoria_id)
        
    result = await db.execute(query)
    return result.scalars().all()

# --- Categorias ---

async def get_all_categorias(db: AsyncSession) -> List[models.CategoriaEquipamento]:
    query = select(models.CategoriaEquipamento).order_by(models.CategoriaEquipamento.nome)
    result = await db.execute(query)
    return result.scalars().all()

# --- Distribuidores (MANTIDO) ---

async def get_all_distribuidores(db: AsyncSession) -> List[models.Distribuidor]:
    query = select(models.Distribuidor).order_by(models.Distribuidor.nome)
    result = await db.execute(query)
    return result.scalars().all()


# --- Cache Helper (Novo) ---

async def _clear_catalogo_cache(redis_client: aioredis.Redis):
    """
    Helper para invalidar o cache da lista do catálogo.
    Chame isso ao Criar, Atualizar ou Deletar um CatalogoItem.
    """
    try:
        print(f"Cache CLEAR: Deletando a chave {CATALOGO_CACHE_KEY}")
        await redis_client.delete(CATALOGO_CACHE_KEY)
    except Exception as e:
        # Logar o erro, mas não travar a operação principal
        print(f"Erro ao limpar cache do Redis: {e}")


# --- Itens de Catálogo (SKUs com preço - MODIFICADO COM CACHE) ---

async def get_all_catalogo_itens(
    db: AsyncSession, 
    redis_client: aioredis.Redis
) -> List[dict]:
    """
    Busca todos os itens do catálogo, implementando o padrão Cache-Aside.
    Retorna uma lista de dicts (pronta para JSON) ao invés de modelos ORM.
    """
    
    # 1. Tentar ler do Cache (Redis)
    try:
        cached_data = await redis_client.get(CATALOGO_CACHE_KEY)
        if cached_data:
            print("Cache HIT: Retornando dados do Redis.")
            # Dados estão armazenados como string JSON, então desserializamos
            return json.loads(cached_data)
    except Exception as e:
        # Se o Redis falhar, logamos o erro e seguimos para o DB
        print(f"Erro ao ler cache do Redis (seguindo para o DB): {e}")

    # 2. Cache MISS: Buscar do Banco de Dados (PostgreSQL)
    print("Cache MISS: Buscando dados do PostgreSQL.")
    query = (
        select(models.CatalogoItem)
        .options(
            joinedload(models.CatalogoItem.equipamento).joinedload(models.Equipamento.categoria),
            joinedload(models.CatalogoItem.distribuidor)
        )
        .order_by(models.CatalogoItem.id.desc())
    )
    result = await db.execute(query)
    itens_orm = result.scalars().all()

    # 3. Serializar os dados para armazenar no cache (Pydantic v2)
    # Convertemos os modelos ORM para dicts usando o schema
    serializable_data = [
        schema.ShowCatalogoItem.model_validate(item).model_dump()
        for item in itens_orm
    ]
    
    # 4. Salvar no Cache (Redis) com TTL
    try:
        # Serializamos a *lista inteira* de dicts para uma string JSON
        json_data = json.dumps(serializable_data, default=str) # default=str para Decimals
        await redis_client.setex(
            CATALOGO_CACHE_KEY,
            CATALOGO_CACHE_TTL_SECONDS,
            json_data
        )
        print("Cache SET: Dados do catálogo salvos no Redis.")
    except Exception as e:
        # Se salvar no cache falhar, apenas logamos
        print(f"Erro ao salvar cache no Redis: {e}")

    # 5. Retornar os dados serializados (lista de dicts)
    return serializable_data


# --- Kits (MANTIDO) ---

async def get_all_kits(db: AsyncSession) -> List[models.Kit]:
    query = (
        select(models.Kit)
        .options(
            joinedload(models.Kit.distribuidor),
            selectinload(models.Kit.itens).joinedload(models.CatalogoItem.equipamento),
        )
        .order_by(models.Kit.nome_kit)
    )
    result = await db.execute(query)
    return result.scalars().all()