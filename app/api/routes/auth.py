from fastapi import APIRouter, Depends
from app.application.use_cases.auth.login import LoginUseCase
from app.api.schemas.auth.login import LoginRequest, LoginResponse
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.api.schemas.auth.refresh import RefreshTokenRequest
from app.core.dependencies import get_login_usecase, get_refresh_token_usecase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(
    request: LoginRequest,
    usecase: LoginUseCase = Depends(get_login_usecase)
):
    token_pair = await usecase.execute(request.email, request.password)
    return LoginResponse(
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
        expires_in=token_pair.expires_in
    )

@router.post("/refresh", response_model=LoginResponse, status_code=200)
async def refresh_token(
    request: RefreshTokenRequest,
    usecase: RefreshTokenUseCase = Depends(get_refresh_token_usecase)
):
    token_pair = await usecase.execute(request.refresh_token)
    return LoginResponse(
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
        expires_in=token_pair.expires_in
    )