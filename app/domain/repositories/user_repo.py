from typing import Optional, Protocol

from ..models.user import User


class UserRepository(Protocol):
    async def create_user(
        self, user_id: int, name: str, email: str, password: str
    ) -> User: ...

    async def get_user_by_id(
            self, user_id: int
    ) -> Optional[User]: ...

    async def get_user_by_email(
            self, email: str
    ) -> Optional[User]: ...

    async def delete_user_by_id(
            self, user_id: int
    ) -> None: ...

    async def update_user_by_id(
            self, user_id: int, name: Optional[str], email: Optional[str]
    ) -> User: ...
    
    async def update_user_password_by_id(
            self, user_id: int, new_password: str
    ) -> None: ...
    
    async def get_user_with_password_by_email(
            self, email: str
    ) -> Optional[User]: ...