from app.application.exceptions import UserExistsException
from app.data.schemas import User
from app.domain.repositories.user_repo import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, name: str, email: str, password: str) -> User:
        user_exists = await self.user_repository.get_user_by_email(email)
        if user_exists:
            raise UserExistsException("Email already in use")

        new_user = await self.user_repository.create_user(name, email, password)
        return new_user