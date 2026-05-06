from pydantic import BaseModel, EmailStr, Field


class UpdatePasswordInput(BaseModel):
    email: EmailStr
    old_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)