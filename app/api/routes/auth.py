from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import LoginRequest, TokenResponse, UserResponse, RefreshTokenRequest, UserLoginResponse
from core.auth.auth_service import JwtAuthService
from core.auth.encryption_service import EncryptionService
from data.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from api.dependencies import get_current_user, get_current_active_user, get_session
from core.dependencies import get_auth_service
from core.domain.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=UserLoginResponse)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_session),
    jwt_service: JwtAuthService = Depends(get_auth_service),
):
    repository = SQLAlchemyUserRepository(session)
    
    user = await repository.get_by_email(login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not EncryptionService.check_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    tokens = jwt_service.generate_jwt_pair(user.id, user.email)
    return UserLoginResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active
        ),
        tokens=TokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type
        )
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    jwt_service: JwtAuthService = Depends(get_auth_service),
):
    try:
        tokens = jwt_service.refresh_jwt_pair(refresh_data.refresh_token)
        return TokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type
        )
    except Exception:
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
        email=current_user.email,
        name=current_user.name,
        is_active=current_user.is_active
    )