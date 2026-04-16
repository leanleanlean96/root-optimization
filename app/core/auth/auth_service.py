import jwt
from datetime import timedelta, datetime, timezone
from .models import UserClaims, JwtTokenPair
from ..exceptions import (
    TokenExpiredException,
    InvalidTokenException,
    InvalidTokenTypeException,
)


class JwtAuthService:
    def __init__(
        self,
        secret: str,
        access_timedelta: timedelta,
        refresh_timedelta: timedelta,
        algorithm: str,
    ) -> None:
        self.secret: str = secret
        self.access_timedelta: timedelta = access_timedelta
        self.refresh_timedelta: timedelta = refresh_timedelta
        self.algorithm = algorithm

    def generate_jwt_pair(self, user_id: int, email: str) -> JwtTokenPair:
        now = datetime.now(timezone.utc)

        access_payload = {
            "sub": user_id,
            "email": email,
            "type": "access",
            "iat": now,
            "exp": now + self.access_timedelta,
        }

        access_token = jwt.encode(access_payload, self.secret, algorithm=self.algorithm)

        refresh_payload = {
            "sub": user_id,
            "email": email,
            "type": "refresh",
            "iat": now,
            "exp": now + self.refresh_timedelta,
        }

        refresh_token = jwt.encode(
            refresh_payload, self.secret, algorithm=self.algorithm
        )

        return JwtTokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=int(self.access_timedelta.total_seconds()),
        )

    def refresh_jwt_pair(self, refresh_token: str) -> JwtTokenPair:
        try:
            payload = jwt.decode(
                refresh_token, self.secret, algorithms=[self.algorithm]
            )
            if payload.get("type") != "refresh":
                raise InvalidTokenTypeException("Provided token is not a refresh token")
            user_id = int(payload.get("sub"))
            email = payload.get("email")
            return self.generate_jwt_pair(user_id, email)
        except jwt.ExpiredSignatureError as err:
            raise TokenExpiredException("Provided refresh token has expired") from err
        except jwt.InvalidTokenError as err:
            raise InvalidTokenException("Provided refresh token is invalid") from err

    def get_payload_data(self, access_token: str) -> UserClaims:
        try:
            payload = jwt.decode(access_token, self.secret, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                raise InvalidTokenTypeException("Provided token is not an access token")
            return UserClaims(
                user_id=payload.get("id"),
                user_email=payload.get("email"),
                type=payload.get("type"),
                iat=payload.get("iat"),
                exp=payload.get("exp"),
            )
        except jwt.ExpiredSignatureError as err:
            raise TokenExpiredException("Provided access token has expired") from err
        except jwt.InvalidTokenError as err:
            raise InvalidTokenException("Provided access token is invalid") from err
