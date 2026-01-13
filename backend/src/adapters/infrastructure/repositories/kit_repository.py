from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from decimal import Decimal

from ....core.application.ports.repositories import IKitRepository
from ....core.domain.orcamentos.entities import Kit, ItemKit
from ....core.domain.orcamentos.value_objects import (
    KitId, ItemId, CategoriaItem, Dinheiro, Quantidade, PotenciaWatts
)
from ..database.models import KitModel, ItemKitModel

class KitRepository(IKitRepository):
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def salvar(self, kit: Kit) -> None:
        # Busca se já existe
        result = await self._session.execute(
            select(KitModel).where(KitModel.id == kit.id)
        )
        kit_model = result.scalar_one_or_none()
        
        if kit_model:
            # Atualiza
            kit_model.nome = kit.nome
            kit_model.is_template = kit.is_template
            
            # Remove itens antigos
            await self._session.execute(
                select(ItemKitModel).where(ItemKitModel.kit_id == kit.id)
            )
            for item_model in kit_model.itens:
                await self._session.delete(item_model)
        else:
            # Cria novo
            kit_model = KitModel(
                id=kit.id,
                nome=kit.nome,
                is_template=kit.is_template
            )
            self._session.add(kit_model)
        
        # Adiciona itens
        for item in kit.itens:
            item_model = ItemKitModel(
                id=item.id,
                kit_id=kit.id,
                categoria=item.categoria.value,
                nome=item.nome,
                marca=item.marca,
                potencia_watts=item.potencia.valor if item.potencia else None,
                preco=item.preco.valor,
                quantidade=item.quantidade.valor,
                descricao=item.descricao
            )
            self._session.add(item_model)
        
        await self._session.commit()
    
    async def buscar_por_id(self, kit_id: KitId) -> Optional[Kit]:
        result = await self._session.execute(
            select(KitModel)
            .options(selectinload(KitModel.itens))
            .where(KitModel.id == kit_id)
        )
        kit_model = result.scalar_one_or_none()
        
        if not kit_model:
            return None
        
        return self._to_domain(kit_model)
    
    async def listar_templates(self) -> List[Kit]:
        result = await self._session.execute(
            select(KitModel)
            .options(selectinload(KitModel.itens))
            .where(KitModel.is_template == True)
        )
        kit_models = result.scalars().all()
        
        return [self._to_domain(km) for km in kit_models]
    
    def _to_domain(self, kit_model: KitModel) -> Kit:
        itens = []
        for item_model in kit_model.itens:
            potencia = PotenciaWatts(item_model.potencia_watts) if item_model.potencia_watts else None
            
            item = ItemKit(
                id=ItemId(str(item_model.id)),
                categoria=CategoriaItem(item_model.categoria),
                nome=item_model.nome,
                marca=item_model.marca,
                potencia=potencia,
                preco=Dinheiro(Decimal(str(item_model.preco))),
                quantidade=Quantidade(item_model.quantidade),
                descricao=item_model.descricao
            )
            itens.append(item)
        
        kit = Kit(
            id=KitId(str(kit_model.id)),
            nome=kit_model.nome,
            itens=itens,
            is_template=kit_model.is_template
        )
        
        return kit
