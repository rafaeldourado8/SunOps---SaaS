from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    @abstractmethod
    def save(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def find_by_id(self, id: UUID) -> Optional[T]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        pass
