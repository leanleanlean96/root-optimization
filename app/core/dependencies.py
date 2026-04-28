from core.auth.auth_service import JwtAuthService
from core.config import config


def get_auth_service() -> JwtAuthService:
    return JwtAuthService(
        secret=config.jwt.secret_key,
        access_timedelta=config.jwt.access_key_delta,
        refresh_timedelta=config.jwt.refresh_key_delta,
        algorithm=config.jwt.algorithm,
    )