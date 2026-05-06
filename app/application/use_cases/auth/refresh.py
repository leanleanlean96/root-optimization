
from app.core.auth.auth_service import JwtAuthService
from app.core.auth.models import JwtTokenPair


class RefreshTokenUseCase:
    def __init__(self, auth_service: JwtAuthService):
        self.auth_service: JwtAuthService = auth_service

    async def execute(self, refresh_token: str) -> JwtTokenPair:
        new_token_pair: JwtTokenPair = self.auth_service.refresh_jwt_pair(refresh_token)
        return new_token_pair