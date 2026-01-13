from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime

from ....core.application.ports.repositories import IOrcamentoRepository
from ....core.domain.orcamentos.aggregates import Orcamento, StatusOrcamento
from ....core.domain.orcamentos.value_objects import OrcamentoId, KitId
from ..database.models import OrcamentoModel, KitModel
from .kit_repository import KitRepository

class OrcamentoRepository(IOrcamentoRepository):
    
    def __init__(self, session: AsyncSession):
        self._session = session
        self._kit_repo = KitRepository(session)
    
    async def salvar(self, orcamento: Orcamento) -> None:
        result = await self._session.execute(
            select(OrcamentoModel).where(OrcamentoModel.id == orcamento.id)
        )
        orc_model = result.scalar_one_or_none()
        
        if orc_model:
            orc_model.status = orcamento.status.value
            orc_model.aprovado_por = orcamento.aprovado_por
            orc_model.enviado_em = orcamento.enviado_em
            orc_model.updated_at = datetime.now()
        else:
            orc_model = OrcamentoModel(
                id=orcamento.id,
                kit_id=orcamento.kit.id,
                cliente_nome=orcamento.cliente_nome,
                cliente_contato=orcamento.cliente_contato,
                status=orcamento.status.value,
                validade_dias=orcamento.validade_dias,
                aprovado_por=orcamento.aprovado_por,
                enviado_em=orcamento.enviado_em
            )
            self._session.add(orc_model)
        
        await self._session.commit()
    
    async def buscar_por_id(self, orcamento_id: OrcamentoId) -> Optional[Orcamento]:
        result = await self._session.execute(
            select(OrcamentoModel)
            .options(selectinload(OrcamentoModel.kit))
            .where(OrcamentoModel.id == orcamento_id)
        )
        orc_model = result.scalar_one_or_none()
        
        if not orc_model:
            return None
        
        return await self._to_domain(orc_model)
    
    async def listar_expirados(self) -> List[Orcamento]:
        result = await self._session.execute(
            select(OrcamentoModel)
            .options(selectinload(OrcamentoModel.kit))
            .where(OrcamentoModel.status.in_(['rascunho', 'em_revisao', 'aprovado']))
        )
        orc_models = result.scalars().all()
        
        orcamentos = []
        for om in orc_models:
            orc = await self._to_domain(om)
            if orc._esta_expirado():
                orcamentos.append(orc)
        
        return orcamentos
    
    async def _to_domain(self, orc_model: OrcamentoModel) -> Orcamento:
        kit = await self._kit_repo.buscar_por_id(KitId(str(orc_model.kit_id)))
        
        orcamento = Orcamento(
            id=OrcamentoId(str(orc_model.id)),
            kit=kit,
            cliente_nome=orc_model.cliente_nome,
            cliente_contato=orc_model.cliente_contato,
            status=StatusOrcamento(orc_model.status),
            validade_dias=orc_model.validade_dias,
            created_at=orc_model.created_at,
            updated_at=orc_model.updated_at,
            aprovado_por=orc_model.aprovado_por,
            enviado_em=orc_model.enviado_em
        )
        
        return orcamento
