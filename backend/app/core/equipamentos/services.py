from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional, Sequence

from . import models, schema

# --- Distribuidor Services ---
async def create_distribuidor(db: AsyncSession, distribuidor: schema.DistribuidorCreate) -> models.Distribuidor:
    db_distribuidor = models.Distribuidor(**distribuidor.model_dump())
    db.add(db_distribuidor)
    await db.commit()
    await db.refresh(db_distribuidor)
    return db_distribuidor

async def get_distribuidor_by_id(db: AsyncSession, distribuidor_id: int) -> Optional[models.Distribuidor]:
    return await db.get(models.Distribuidor, distribuidor_id)

async def get_distribuidor_by_nome(db: AsyncSession, nome: str) -> Optional[models.Distribuidor]:
    result = await db.execute(select(models.Distribuidor).where(models.Distribuidor.nome == nome))
    return result.scalars().first()

async def get_all_distribuidores(db: AsyncSession) -> Sequence[models.Distribuidor]:
    result = await db.execute(select(models.Distribuidor).order_by(models.Distribuidor.nome))
    return result.scalars().all()

# --- CategoriaEquipamento Services ---
async def create_categoria(db: AsyncSession, categoria: schema.CategoriaEquipamentoCreate) -> models.CategoriaEquipamento:
    db_categoria = models.CategoriaEquipamento(**categoria.model_dump())
    db.add(db_categoria)
    await db.commit()
    await db.refresh(db_categoria)
    return db_categoria

async def get_categoria_by_id(db: AsyncSession, categoria_id: int) -> Optional[models.CategoriaEquipamento]:
    # Exemplo carregando subcategorias (pode ser útil)
    # query = select(models.CategoriaEquipamento).options(selectinload(models.CategoriaEquipamento.subcategorias)).where(models.CategoriaEquipamento.id == categoria_id)
    # result = await db.execute(query)
    # return result.scalars().first()
     return await db.get(models.CategoriaEquipamento, categoria_id)


async def get_all_categorias(db: AsyncSession) -> Sequence[models.CategoriaEquipamento]:
    # Poderia carregar hierarquia aqui se necessário
    result = await db.execute(select(models.CategoriaEquipamento).order_by(models.CategoriaEquipamento.nome))
    return result.scalars().all()

# --- Equipamento Services ---
async def create_equipamento(db: AsyncSession, equipamento: schema.EquipamentoCreate) -> models.Equipamento:
    db_equipamento = models.Equipamento(**equipamento.model_dump())
    db.add(db_equipamento)
    await db.commit()
    await db.refresh(db_equipamento)
    return db_equipamento

async def get_equipamento_by_id(db: AsyncSession, equipamento_id: int) -> Optional[models.Equipamento]:
    # Carrega a categoria junto
    query = select(models.Equipamento).options(joinedload(models.Equipamento.categoria)).where(models.Equipamento.id == equipamento_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_all_equipamentos(db: AsyncSession, categoria_id: Optional[int] = None) -> Sequence[models.Equipamento]:
    query = select(models.Equipamento).options(joinedload(models.Equipamento.categoria)).order_by(models.Equipamento.nome_modelo)
    if categoria_id:
        query = query.where(models.Equipamento.categoria_id == categoria_id)
    result = await db.execute(query)
    return result.scalars().all()

# --- CatalogoItem Services ---
async def create_catalogo_item(db: AsyncSession, item: schema.CatalogoItemCreate) -> models.CatalogoItem:
    db_item = models.CatalogoItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    # Recarrega com relacionamentos para retornar dados completos
    return await get_catalogo_item_by_id(db, db_item.id)


async def get_catalogo_item_by_id(db: AsyncSession, item_id: int) -> Optional[models.CatalogoItem]:
    query = select(models.CatalogoItem).options(
        joinedload(models.CatalogoItem.equipamento),
        joinedload(models.CatalogoItem.distribuidor)
    ).where(models.CatalogoItem.id == item_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_all_catalogo_itens(
    db: AsyncSession,
    equipamento_id: Optional[int] = None,
    distribuidor_id: Optional[int] = None
) -> Sequence[models.CatalogoItem]:
    query = select(models.CatalogoItem).options(
        joinedload(models.CatalogoItem.equipamento), #.joinedload(models.Equipamento.categoria), # Exemplo de load aninhado
        joinedload(models.CatalogoItem.distribuidor)
    ).order_by(models.CatalogoItem.id) # Ou ordenar por equipamento.nome_modelo

    if equipamento_id:
        query = query.where(models.CatalogoItem.equipamento_id == equipamento_id)
    if distribuidor_id:
        query = query.where(models.CatalogoItem.distribuidor_id == distribuidor_id)

    result = await db.execute(query)
    return result.scalars().all()


# --- Kit Services ---
# Estes são mais complexos devido à relação Many-to-Many

async def create_kit(db: AsyncSession, kit_data: schema.KitCreate) -> models.Kit:
    # 1. Cria o Kit base sem os itens
    kit_dict = kit_data.model_dump(exclude={'itens'})
    db_kit = models.Kit(**kit_dict)
    db.add(db_kit)
    await db.flush() # Gera o ID do kit antes de adicionar itens

    # 2. Adiciona os itens associados (requer buscar os objetos CatalogoItem)
    if kit_data.itens:
        for item_assoc in kit_data.itens:
            catalogo_item = await db.get(models.CatalogoItem, item_assoc.catalogo_item_id)
            if catalogo_item:
                 # A associação Many-to-Many é feita através da lista 'itens' no modelo Kit
                 # Precisamos adicionar o objeto CatalogoItem à lista
                 db_kit.itens.append(catalogo_item)
                 # A tabela de associação precisa da quantidade, como fazer isso?
                 # SQLAlchemy lida com isso se a tabela de associação for definida corretamente
                 # com uma coluna 'quantidade'. Precisamos garantir que 'kit_items_association' a tenha.
                 # E como atribuir a quantidade específica?
                 # Uma forma comum é usar uma "Association Proxy" ou gerenciar a tabela de associação diretamente.
                 # Por simplicidade aqui, vamos assumir que a relação 'itens' é suficiente,
                 # mas a quantidade pode precisar de um manejo especial (talvez após o commit).

    await db.commit()
    await db.refresh(db_kit)
    # Recarrega com os itens para retornar completo
    return await get_kit_by_id(db, db_kit.id)


async def get_kit_by_id(db: AsyncSession, kit_id: int) -> Optional[models.Kit]:
    query = select(models.Kit).options(
        joinedload(models.Kit.distribuidor),
        selectinload(models.Kit.itens) # Use selectinload para ManyToMany
            .joinedload(models.CatalogoItem.equipamento) # Carrega equipamento dentro do item
    ).where(models.Kit.id == kit_id)
    result = await db.execute(query)
    kit = result.scalars().first()

    # Precisamos carregar a quantidade da tabela de associação separadamente ou ajustar o modelo/query
    # Vamos deixar isso para um refinamento posterior por enquanto.
    return kit


async def get_all_kits(db: AsyncSession, distribuidor_id: Optional[int] = None) -> Sequence[models.Kit]:
    query = select(models.Kit).options(
        joinedload(models.Kit.distribuidor),
        selectinload(models.Kit.itens).joinedload(models.CatalogoItem.equipamento) # Carrega itens e seus equipamentos
    ).order_by(models.Kit.nome_kit)

    if distribuidor_id:
        query = query.where(models.Kit.distribuidor_id == distribuidor_id)

    result = await db.execute(query)
    # Novamente, a quantidade da tabela de associação pode precisar ser carregada separadamente.
    return result.scalars().all()

# Adicione funções para update e delete conforme necessário...