from abc import ABC, abstractmethod
from core.domain.models.user import User
from typing import Optional, List

class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        ...
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        ...
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        ...
        
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        ...