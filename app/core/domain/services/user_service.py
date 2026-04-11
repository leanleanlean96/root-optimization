from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository
from core.domain.exceptions import BusinessError
from core.config import config
from api.shemas import UserUpdate

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
            print(f"User not found: {email}")
            return None
        
        print(f"User found: {email}")
        print(f"Password from DB (hash): {user.password.password}")
        print(f"Password input: {password}")
        print(f"Password input length: {len(password)}")
        
        is_valid = user.verify_password(password)
        print(f"Password valid: {is_valid}")
        
        if not is_valid:
            return None
        
        if not user.is_active:
            raise BusinessError("User account is not active")
        
        return user
    
    def create_access_token(self, user: User) -> str:
        """Создание access токена"""
        expire = datetime.utcnow() + timedelta(minutes=config.jwt.access_token_expire_minutes)
        to_encode = {
            "sub": user.email.email,
            "user_id": user.id,
            "exp": expire,
            "type": "access"
        }
        encoded_jwt = jwt.encode(to_encode, config.jwt.secret_key, algorithm=config.jwt.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, user: User) -> str:
        """Создание refresh токена"""
        expire = datetime.utcnow() + timedelta(days=config.jwt.refresh_token_expire_days)
        to_encode = {
            "sub": user.email.email,
            "user_id": user.id,
            "exp": expire,
            "type": "refresh"
        }
        encoded_jwt = jwt.encode(to_encode, config.jwt.secret_key, algorithm=config.jwt.algorithm)
        return encoded_jwt
    
    def create_tokens(self, user: User) -> dict:
        """Создание пары токенов"""
        return {
            "access_token": self.create_access_token(user),
            "refresh_token": self.create_refresh_token(user),
            "token_type": "bearer"
        }
    
    def decode_token(self, token: str) -> dict:
        """Декодирование и валидация токена"""
        try:
            payload = jwt.decode(
                token, 
                config.jwt.secret_key, 
                algorithms=[config.jwt.algorithm]
            )
            return payload
        except JWTError as e:
            raise BusinessError(f"Invalid token: {str(e)}")
        
    def refresh_access_token(self, refresh_token: str) -> str:
        """Обновление access токена по refresh токену"""
        payload = self.decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise BusinessError("Invalid token type")
        
        expire = datetime.utcnow() + timedelta(minutes=config.jwt.access_token_expire_minutes)
        new_payload = {
            "sub": payload.get("sub"),
            "user_id": payload.get("user_id"),
            "exp": expire,
            "type": "access"
        }
        new_access_token = jwt.encode(new_payload, config.jwt.secret_key, algorithm=config.jwt.algorithm)
        return new_access_token


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
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None
        
        if user_update.name:
            user.change_name(user_update.name)
        
        if user_update.email:
            user.change_email(user_update.email)
        
        if user_update.password:
            user.change_password(user_update.password)
        
        return await self.repository.save(user)
    
    async def delete(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)