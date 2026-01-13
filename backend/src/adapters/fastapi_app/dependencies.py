from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.database.config import AsyncSessionLocal
from ..infrastructure.repositories.kit_repository import KitRepository
from ..infrastructure.repositories.orcamento_repository import OrcamentoRepository

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

def get_kit_repository(session: AsyncSession) -> KitRepository:
    return KitRepository(session)

def get_orcamento_repository(session: AsyncSession) -> OrcamentoRepository:
    return OrcamentoRepository(session)
