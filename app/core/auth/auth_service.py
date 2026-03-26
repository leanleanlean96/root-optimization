import jwt
from datetime import timedelta, datetime, timezone


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

    def generate_jwt_pair(self, user_id: int) -> dict:
        now = datetime.now(timezone.utc)

        access_payload = {
            "sub": user_id,
            "type": "access",
            "iat": now,
            "exp": now + self.access_timedelta,
        }

        access_token = jwt.encode(access_payload, self.secret, algorithm=self.algorithm)

        refresh_payload = {
            "sub": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + self.refresh_timedelta,
        }

        refresh_token = jwt.encode(
            refresh_payload, self.secret, algorithm=self.algorithm
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": int(self.access_timedelta.total_seconds()),
        }

    def refresh_jwt_pair(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(
                refresh_token, self.secret, algorithms=[self.algorithm]
            )
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")
            user_id = int(payload.get("sub"))
            return self.generate_jwt_pair(user_id)
        except jwt.ExpiredSignatureError as err:
            raise ValueError("Provided refresh token has expired") from err
        except jwt.InvalidTokenError as err:
            raise ValueError("Provided refresh token is invalid") from err

    def get_payload_data(self, access_token: str) -> dict:
        try:
            payload = jwt.decode(access_token, self.secret, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                raise ValueError("Provided token is not an access token")
            return payload
        except jwt.ExpiredSignatureError as err:
            raise ValueError("Provided access token has expired") from err
        except jwt.InvalidTokenError as err:
            raise ValueError("Provided access token is invalid") from err
