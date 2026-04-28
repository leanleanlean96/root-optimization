from typing import Protocol, Optional

from core.domain.models.user import User


class UserRepository(Protocol):
    async def save(self, user: User) -> User: 
        ...
    
    async def get_by_email(self, email: str) -> Optional[User]: 
        ...
    
    async def get_by_id(self, user_id: int) -> Optional[User]: 
        ...
    
    async def delete(self, user_id: int) -> bool: 
        ...
    
    async def exists_by_email(self, email: str) -> bool: 
        ...