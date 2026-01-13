from abc import ABC, abstractmethod
from typing import Optional
import uuid

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, email: str, hashed_password: str, full_name: str) -> dict:
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[dict]:
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: uuid.UUID) -> Optional[dict]:
        pass
