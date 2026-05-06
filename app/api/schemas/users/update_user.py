from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UpdateUserInput(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=33, default=None)
    email: Optional[EmailStr] = Field(default=None)