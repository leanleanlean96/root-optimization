from pydantic import BaseModel, EmailStr, Field



class UserResponse(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=33)
    email: EmailStr
    is_active: bool = Field(default=True)
