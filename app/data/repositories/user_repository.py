from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.domain.models.user import User
from app.application.models.auth_user import AuthUser
from ..schemas import User as UserData


class UserRepository():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self, name: str, email: str, password: str
    ) -> User: 
        db_user: UserData = UserData(
            name=name,
            email=email,
            password=password,
            is_active=True
        )

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            is_active=db_user.is_active
        )
    
    async def get_user_by_id(
            self, user_id: int
    ) -> Optional[User]:
        query_result = await self.session.execute(
            select(UserData).where(UserData.id == user_id, UserData.is_active == True)
        )

        db_user = query_result.scalar_one_or_none()
        if db_user is None:
            return None
        
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            is_active=db_user.is_active
        )
    
    async def get_user_by_email(
            self, email: str
    ) -> Optional[User]:
        query_result = await self.session.execute(
            select(UserData).where(UserData.email == email, UserData.is_active == True)
        )

        db_user = query_result.scalar_one_or_none()
        if db_user is None:
            return None
        
        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            is_active=db_user.is_active
        )
    
    async def delete_user_by_id(
            self, user_id: int
    ) -> None:
        query_result = await self.session.execute(
            select(UserData).where(UserData.id == user_id, UserData.is_active == True)
        )

        db_user = query_result.scalar_one_or_none()
        if db_user is None:
            return
        
        db_user.is_active = False
        self.session.add(db_user)
        await self.session.commit()

    async def update_user_by_id(
            self, user_id: int, name: Optional[str], email: Optional[str]
    ) -> User:
        query_result = await self.session.execute(
            select(UserData).where(UserData.id == user_id, UserData.is_active == True)
        )

        db_user = query_result.scalar_one_or_none()
        if db_user is None:
            return None
        
        if name is not None:
            db_user.name = name
        
        if email is not None:
            db_user.email = email

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        return User(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            is_active=db_user.is_active
        )
    
    async def update_user_password_by_id(
            self, user_id: int, new_password: str
    ) -> None:
        query_result = await self.session.execute(
            select(UserData).where(UserData.id == user_id, UserData.is_active == True)
        )

        db_user = query_result.scalar_one_or_none()
        if db_user is None:
            return
        
        db_user.password = new_password
        self.session.add(db_user)
        await self.session.commit()

    async def get_user_with_password_by_email(
            self, email: str
    ) -> Optional[User]:
        query_result = await self.session.execute(
            select(UserData).where(UserData.email == email, UserData.is_active == True)
        )

        db_user = query_result.scalar_one_or_none()
        if db_user is None:
            return None
        
        return AuthUser(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            password=db_user.password,
            is_active=db_user.is_active
        )