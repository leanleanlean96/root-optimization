from app.domain.repositories.user_repo import UserRepository
from app.core.auth.encryption_service import EncryptionService
from app.application.exceptions import UserNotFoundException, UnauthorizedException

class UpdateUserPasswordUseCase:
    def __init__(self, user_repository: UserRepository, encryption_service: EncryptionService):
        self.user_repository = user_repository
        self.encryption_service: EncryptionService = encryption_service

    async def execute(self, email: str, old_password: str, new_password: str) -> None:
        user = await self.user_repository.get_user_with_password_by_email(email)
        if not user:
            raise UserNotFoundException(f"User not found")

        if not self.encryption_service.check_password(old_password, user.password):
            raise UnauthorizedException("Old password is incorrect")

        await self.user_repository.update_user_password_by_id(user.id, self.encryption_service.hash_password(new_password))