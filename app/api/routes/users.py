from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserCreate, UserResponse, UserUpdate
from core.auth.encryption_service import EncryptionService
from core.domain.models.user import User
from data.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from api.dependencies import get_current_active_user, get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    repository = SQLAlchemyUserRepository(session)

    if await repository.exists_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = EncryptionService.hash_password(user_create.password)
    user = User.register(user_create.name, user_create.email, hashed_password)
    saved_user = await repository.save(user)
    
    return UserResponse(
        id=saved_user.id,
        email=saved_user.email,
        name=saved_user.name,
        is_active=saved_user.is_active
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    repository = SQLAlchemyUserRepository(session)
    user = await repository.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        is_active=user.is_active
    )


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    repository = SQLAlchemyUserRepository(session)
    
    existing_user = await repository.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    if user_data.email is not None and user_data.email != existing_user.email:
        if await repository.exists_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        existing_user.email = user_data.email
    
    if user_data.name is not None:
        existing_user.name = user_data.name
    
    if user_data.password is not None:
        existing_user.password = EncryptionService.hash_password(user_data.password)
    
    saved_user = await repository.save(existing_user)
    
    return UserResponse(
        id=saved_user.id,
        email=saved_user.email,
        name=saved_user.name,
        is_active=saved_user.is_active
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    repository = SQLAlchemyUserRepository(session)
    
    if not await repository.delete(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    return None