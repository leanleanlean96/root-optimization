from dataclasses import dataclass

from app.core.domain.repositories.user_repository import UserRepository
from app.core.domain.models.user import User
from app.core.auth.encryption_service import EncryptionService
from app.core.auth.auth_service import JwtAuthService
from app.core.auth.models import JwtTokenPair


@dataclass
class RegisterUserInput:
    name: str
    email: str
    password: str


@dataclass
class RegisterUserOutput:
    id: int
    email: str
    name: str
    is_active: bool


@dataclass
class AuthenticateUserInput:
    email: str
    password: str


@dataclass
class AuthenticateUserOutput:
    id: int
    email: str
    name: str
    is_active: bool
    tokens: JwtTokenPair


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    async def execute(self, input: RegisterUserInput) -> RegisterUserOutput:
        if await self.user_repo.exists_by_email(input.email):
            raise ValueError("Email already registered")
        
        hashed_password = EncryptionService.hash_password(input.password)
        user = User.register(input.name, input.email, hashed_password)
        saved_user = await self.user_repo.save(user)
        
        return RegisterUserOutput(
            id=saved_user.id,
            email=saved_user.email,
            name=saved_user.name,
            is_active=saved_user.is_active,
        )


class AuthenticateUserUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        jwt_service: JwtAuthService,
    ):
        self.user_repo = user_repo
        self.jwt_service = jwt_service

    async def execute(self, input: AuthenticateUserInput) -> AuthenticateUserOutput:
        user = await self.user_repo.get_by_email(input.email)
        if not user:
            raise ValueError("Invalid credentials")
        
        if not EncryptionService.check_password(input.password, user.password):
            raise ValueError("Invalid credentials")
        
        if not user.is_active:
            raise ValueError("User account is not active")
        
        tokens = self.jwt_service.generate_jwt_pair(user.id, user.email)
        
        return AuthenticateUserOutput(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            tokens=tokens,
        )