from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthUser:
    id: int
    name: str
    email: str
    password: str
    is_active: bool