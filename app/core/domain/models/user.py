from dataclasses import dataclass


@dataclass
class User:
    id: int | None
    email: str
    name: str
    password: str
    is_active: bool = True

    @staticmethod
    def register(name: str, email: str, hashed_password: str) -> "User":
        return User(
            id=None,
            name=name,
            email=email,
            password=hashed_password,
            is_active=True
        )