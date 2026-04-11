from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    """Модель для ответа с токенами"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Полезная нагрузка JWT токена"""
    sub: str
    exp: datetime
    type: str
    user_id: Optional[int] = None


class TokenData(BaseModel):
    """Данные извлеченные из токена"""
    user_id: int
    email: str