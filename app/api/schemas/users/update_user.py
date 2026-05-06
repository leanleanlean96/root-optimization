from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UpdateUserInput(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=33, default=None)
    email: Optional[EmailStr] = Field(default=None)