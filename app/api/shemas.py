from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from core.domain.models.user import Email, User

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    password: Optional[str] = Field(None, min_length=8)