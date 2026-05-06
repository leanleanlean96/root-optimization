from pydantic import BaseModel, Field, EmailStr


class CreateUserInput(BaseModel):
    name: str = Field(min_length=1, max_length=33)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)