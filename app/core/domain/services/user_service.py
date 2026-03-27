from abc import ABC, abstractmethod
from typing import Optional
from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from domain.exceptions import BusinessError

class UserRegistrationService:
    def __init__(self, user_repository: UserRepository
    ):
        self.user_repository = user_repository
    
    async def register(self, user_name: str, email: str, password: str) -> User:
        exists = await self.user_repository.exists_by_email(email)
        if exists:
            raise BusinessError("Email already registered")
        
        user = User.register(user_name, email, password)
        saved_user = await self.user_repository.save(user)
        
        return saved_user


class UserAuthenticationService:
    """
    Доменный сервис для аутентификации.
    Проверяет пароль и возвращает пользователя.
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def authenticate(self, email: str, password: str) -> User | None:
        """Аутентификация пользователя"""
        
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        
        if not user.verify_password(password):
            return None
        
        if not user.is_active:
            raise ValueError("User account is not active")
        
        return user


class UserDuplicateCheckService:
    """
    Доменный сервис — проверка дубликатов.
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def is_email_unique(self, email: str) -> bool:
        """Проверка уникальности email"""
        return not await self.user_repository.exists_by_email(email)
    
class UserApiService:
    """Сервис для API операций с пользователями"""
    
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        return await self.repository.get_by_id(user_id)
    
    async def update_user(self, user_id: int, user_update) -> Optional[User]:
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None
        
        if user_update.name:
            user.change_name(user_update.name)
        
        if user_update.email:
            user.change_email(user_update.email)
        
        if hasattr(user_update, 'password') and user_update.password:
            user.change_password(user_update.password)
        
        return await self.repository.save(user)
    
    async def delete(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)