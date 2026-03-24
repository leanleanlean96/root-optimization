from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from data.schemas import User
from api.shemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_create: UserCreate) -> User:
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            is_active=True
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_name(self, name: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.name == name)
        )
        return result.scalar_one_or_none()

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit).order_by(User.id)
        )
        return list(result.scalars().all())

    async def exists_by_email(self, email: str) -> bool:
        result = await self.db.execute(
            select(func.count(User.id)).where(User.email == email)
        )
        count = result.scalar()
        return count is not None and count > 0

    async def exists_by_name(self, name: str) -> bool:
        result = await self.db.execute(
            select(func.count(User.id)).where(User.name == name)
        )
        count = result.scalar()
        return count is not None and count > 0

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None and hasattr(db_user, key):
                setattr(db_user, key, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete(self, user_id: int) -> bool:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return False
        await self.db.delete(db_user)
        await self.db.commit()
        return True

    async def soft_delete(self, user_id: int) -> Optional[User]:
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None
        db_user.is_active = False
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user