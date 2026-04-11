from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.shemas import LoginRequest, TokenResponse, UserResponse, RefreshTokenRequest, UserLoginResponse
from core.domain.services.user_service import UserAuthenticationService, UserApiService
from core.domain.exceptions import BusinessError
from data.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from api.dependencies import get_current_user, get_current_active_user, get_session
from core.domain.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=UserLoginResponse)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyUserRepository(session)
    auth_service = UserAuthenticationService(repository)
    
    user = await auth_service.authenticate(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens = auth_service.create_tokens(user)
    return UserLoginResponse(
        user=UserResponse(
            id=user.id,
            email=user.email.email,
            name=user.user_name.name,
            is_active=user.is_active
        ),
        tokens=TokenResponse(**tokens)
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session)
):
    repository = SQLAlchemyUserRepository(session)
    auth_service = UserAuthenticationService(repository)
    
    try:
        payload = auth_service.decode_token(refresh_data.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        if not isinstance(user_id, int):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_id must be integer"
            )

        user = await repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if user.email.email != payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token user mismatch"
            )
        
        new_access_token = auth_service.refresh_access_token(refresh_data.refresh_token)
        new_refresh_token = auth_service.create_refresh_token(user)
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
        
    except BusinessError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email.email,
        name=current_user.user_name.name,
        is_active=current_user.is_active
    )