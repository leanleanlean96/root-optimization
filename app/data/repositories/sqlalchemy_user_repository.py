from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.engine import CursorResult
from typing import Optional

from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository

from data.schemas import User as UserModel


class SQLAlchemyUserRepository(UserRepository):
    """Реализация репозитория на SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            password=user_model.password,
            is_active=user_model.is_active,
        )
    
    def _to_model(self, user: User) -> UserModel:
        """Преобразовать доменную сущность в ORM модель"""
        return UserModel(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            is_active=user.is_active,
        )
    
    async def save(self, user: User) -> User:
        """Сохранить пользователя"""
        user_model = self._to_model(user)
        
        if user.id is None:
            self.session.add(user_model)
            await self.session.flush()
            user.id = user_model.id
        else:
            await self.session.merge(user_model)
            await self.session.flush()
        
        await self.session.commit()
        
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            return None
        
        return self._to_domain(user_model)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            return None
        
        return self._to_domain(user_model)
    
    async def exists_by_email(self, email: str) -> bool:
        result = await self.session.execute(
            select(UserModel.id).where(UserModel.email == email)
        )
        return result.scalar_one_or_none() is not None
    
    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        await self.session.execute(
            delete(UserModel).where(UserModel.id == user_id)
        )
        await self.session.commit()
        return True