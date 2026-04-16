from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class UserClaims:
    user_id: str
    user_email: str
    type: str
    iat: datetime
    exp: datetime


@dataclass(frozen=True, slots=True)
class JwtTokenPair:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
