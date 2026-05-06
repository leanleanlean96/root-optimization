from fastapi import APIRouter, Depends, Path, Response

from app.api.schemas.users.create_user import CreateUserInput
from app.api.schemas.users.update_user import UpdateUserInput
from app.api.schemas.users.update_password import UpdatePasswordInput
from app.application.use_cases.users.get_user import GetUserUseCase
from app.api.schemas.users.user_response import UserResponse
from app.application.use_cases.users.create_user import CreateUserUseCase
from app.application.use_cases.users.update_user import UpdateUserUseCase
from app.application.use_cases.users.delete_user import DeleteUserUseCase
from app.application.use_cases.users.update_user_password import UpdateUserPasswordUseCase
from app.core.auth.models import UserClaims
from app.data.schemas import User
from app.core.dependencies import get_create_user_usecase, get_get_user_usecase, get_update_user_usecase, get_delete_user_usecase, get_update_user_password_usecase
from app.core.dependencies import get_user_claims
from app.core.dependencies import get_encryption_service
from app.core.auth.encryption_service import EncryptionService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserResponse, status_code=201)
async def create_user(
    body: CreateUserInput,
    usecase: CreateUserUseCase = Depends(get_create_user_usecase),
    encryption_service: EncryptionService = Depends(get_encryption_service),
):
    result: User = await usecase.execute(
        name=body.name,
        email=body.email,
        password=encryption_service.hash_password(body.password),
    )
    return UserResponse(
        id=result.id,
        name=result.name,
        email=result.email,
    )

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def get_user_by_id(
    user_id: int = Path(gt=0),
    usecase: GetUserUseCase = Depends(get_get_user_usecase),
    claims: UserClaims = Depends(get_user_claims),
):
    result: User = await usecase.execute(user_id)
    return UserResponse(
        id=result.id,
        name=result.name,
        email=result.email
    )

@router.put("/update", response_model=UserResponse, status_code=200)
async def update_user(
    body: UpdateUserInput,
    claims: UserClaims = Depends(get_user_claims),
    usecase: UpdateUserUseCase = Depends(get_update_user_usecase),
):
    updated_user: User = await usecase.execute(
        user_id=claims.user_id,
        name=body.name,
        email=body.email,
    )
    return UserResponse(
        id=updated_user.id,
        name=updated_user.name,
        email=updated_user.email,
    )

@router.delete("/delete", status_code=204)
async def delete_user(
    claims: UserClaims = Depends(get_user_claims),
    usecase: DeleteUserUseCase = Depends(get_delete_user_usecase),
):
    await usecase.execute(claims.user_id)
    return Response(status_code=204)

@router.put("/update_pwd", status_code=204)
async def update_user_password(
    body: UpdatePasswordInput,
    usecase: UpdateUserPasswordUseCase = Depends(get_update_user_password_usecase),
):

    await usecase.execute(
        email=body.email,
        old_password=body.old_password,
        new_password=body.new_password,
    )
    return Response(status_code=204)