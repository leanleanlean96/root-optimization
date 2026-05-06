from typing import Optional

from app.application.exceptions import UserExistsException, UserNotFoundException


class UpdateUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None):
        existing_user = await self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            raise UserNotFoundException()

        if email is not None and existing_user.email != email:
            user_with_email = await self.user_repository.get_user_by_email(email)
            if user_with_email and user_with_email.id != user_id:
                raise UserExistsException("Email is already in use")
            
        if name is None:
            name = existing_user.name
        if email is None:
            email = existing_user.email

        updated_user = await self.user_repository.update_user_by_id(user_id, name, email)
        return updated_user