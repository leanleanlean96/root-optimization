from ...exceptions import UserNotFoundException

class GetUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, user_id: int):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User not found")
        return user