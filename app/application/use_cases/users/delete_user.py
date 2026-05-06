class DeleteUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> None:
        await self.user_repository.delete_user_by_id(user_id)