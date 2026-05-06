from app.core.auth.auth_service import JwtAuthService
from app.core.auth.encryption_service import EncryptionService
from app.core.auth.models import JwtTokenPair
from app.core.exceptions import UnauthorizedException
from app.data.repositories.user_repository import UserRepository


class LoginUseCase:
    def __init__(self, auth_service: JwtAuthService, encryption_service: EncryptionService, user_repository: UserRepository):
        self.auth_service: JwtAuthService = auth_service
        self.encryption_service: EncryptionService = encryption_service
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> JwtTokenPair:
        user = await self.user_repository.get_user_by_email(email)
        if user is None:
            raise UnauthorizedException("Invalid email or password")
        
        if not self.encryption_service.check_password(password, user.password):
            raise UnauthorizedException("Invalid email or password")

        token_pair: JwtTokenPair = self.auth_service.generate_jwt_pair(user.id, email)
        return token_pair