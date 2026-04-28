from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import PyJWTError

from core.auth.auth_service import JwtAuthService
from core.config import config
from core.exceptions import InvalidTokenException, InvalidTokenTypeException, TokenExpiredException, UnauthorizedException
from data.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from api.dependencies.db import get_session
from core.dependencies import get_auth_service


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
    jwt_service: JwtAuthService = Depends(get_auth_service),
):
    token = credentials.credentials
    repository = SQLAlchemyUserRepository(session)
    
    try:
        payload = jwt_service.get_payload_data(token)
        
        user = await repository.get_by_id(payload.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        return user
        
    except (TokenExpiredException, InvalidTokenException, InvalidTokenTypeException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user