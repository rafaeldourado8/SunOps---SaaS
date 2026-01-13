from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid
from ....core.application.ports.user_repository import IUserRepository
from ..database.models import UserModel

class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def create(self, email: str, hashed_password: str, full_name: str) -> dict:
        user = UserModel(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return self._to_dict(user)
    
    async def find_by_email(self, email: str) -> Optional[dict]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = result.scalar_one_or_none()
        return self._to_dict(user) if user else None
    
    async def find_by_id(self, user_id: uuid.UUID) -> Optional[dict]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        return self._to_dict(user) if user else None
    
    def _to_dict(self, user: UserModel) -> dict:
        return {
            "id": user.id,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at
        }
