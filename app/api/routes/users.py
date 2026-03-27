from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from data.dbclient import db_client
from api.shemas import UserCreate, UserResponse, UserUpdate
from core.domain.services.user_service import UserRegistrationService, UserApiService
from data.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

router = APIRouter(prefix="/users", tags=["users"])


async def get_session():
    async for session in db_client.session_getter():
        yield session


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    repository = SQLAlchemyUserRepository(session)
    service = UserRegistrationService(repository)

    if await repository.exists_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = await service.register(user_create.name, user_create.email, user_create.password)
    
    return UserResponse(
        id=user.id,
        email=user.email.email,
        name=user.user_name.name,
        is_active=user.is_active
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    repository = SQLAlchemyUserRepository(session)
    service = UserApiService(repository)
    user = await service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email.email,
        name=user.user_name.name,
        is_active=user.is_active
    )


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyUserRepository(session)
    service = UserApiService(repository)
    
    existing_user = await service.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    if user_data.email and user_data.email != existing_user.email.email:
        if await repository.exists_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user = await service.update_user(user_id, user_data)


    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email.email,
        name=user.user_name.name,
        is_active=user.is_active
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    repository = SQLAlchemyUserRepository(session)
    service = UserApiService(repository)
    
    if not await service.delete(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return None