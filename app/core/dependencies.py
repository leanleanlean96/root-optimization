from typing import AsyncGenerator

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.routes.create_route import CreateRouteUseCase
from app.application.use_cases.routes.delete_route import DeleteRouteUseCase
from app.application.use_cases.routes.generate_random_coordinates import (
    GenerateRandomCoordinatesUseCase,
)
from app.application.use_cases.routes.get_route import GetRouteByIdUseCase
from app.application.use_cases.routes.get_route_metrics import GetRouteMetricsUseCase
from app.application.use_cases.routes.optimize_route import OptimizeRouteUseCase
from app.application.use_cases.users.create_user import CreateUserUseCase
from app.application.use_cases.users.delete_user import DeleteUserUseCase
from app.application.use_cases.users.get_user import GetUserUseCase
from app.application.use_cases.users.update_user import UpdateUserUseCase
from app.application.use_cases.users.update_user_password import (
    UpdateUserPasswordUseCase,
)
from app.core.auth.auth_service import JwtAuthService
from app.core.auth.encryption_service import EncryptionService
from app.core.auth.models import UserClaims
from app.core.config import config
from app.core.exceptions import (
    InvalidTokenException,
    InvalidTokenTypeException,
    TokenExpiredException,
)
from app.application.exceptions import UnauthorizedException
from app.data.repositories.routes_repository import RouteRepository
from app.data.repositories.user_repository import UserRepository
from app.domain.models.coordinate import BoundingBox
from app.domain.services.coordinate_generator_service import (
    CoordinateGenerator as CoordinateGeneratorService,
)
from app.infrastructure.coordinate_generator import (
    CoordinateGenerator,
)
from app.infrastructure.osrm_client import OsrmClient

http_bearer = HTTPBearer(auto_error=True)

async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async for session in request.app.state.db_client.session_getter():
        yield session


async def get_http_client(request: Request) -> AsyncGenerator[AsyncClient, None]:
    yield request.app.state.http_client


def get_auth_service() -> JwtAuthService:
    return JwtAuthService(
        secret=config.jwt.secret_key,
        access_timedelta=config.jwt.access_key_delta,
        refresh_timedelta=config.jwt.refresh_key_delta,
        algorithm=config.jwt.algorithm,
    )

def get_encryption_service() -> EncryptionService:
    return EncryptionService()


def get_user_claims(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: JwtAuthService = Depends(get_auth_service),
) -> UserClaims:
    try:
        return auth_service.get_payload_data(credentials.credentials)
    except TokenExpiredException as e:
        raise UnauthorizedException(f"Unauthorized: {e}")
    except (InvalidTokenException, InvalidTokenTypeException) as e:
        raise UnauthorizedException(f"Unauthorized: {e}")


def get_osrm_client(
    service_url: str = config.osrm.url,
    client: AsyncClient = Depends(get_http_client),
) -> OsrmClient:
    return OsrmClient(service_url, client)

def get_user_repo(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(session)

def get_login_usecase(
    auth_service: JwtAuthService = Depends(get_auth_service),
    encryption_service: EncryptionService = Depends(get_encryption_service),
    user_repository: UserRepository = Depends(get_user_repo),
) -> LoginUseCase:
    return LoginUseCase(auth_service=auth_service, encryption_service=encryption_service, user_repository=user_repository)

def get_refresh_token_usecase(
    auth_service: JwtAuthService = Depends(get_auth_service),
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(auth_service=auth_service)

def get_create_user_usecase(
    user_repo: UserRepository = Depends(get_user_repo),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repository=user_repo)

def get_update_user_usecase(
    user_repo: UserRepository = Depends(get_user_repo),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repository=user_repo)

def get_get_user_usecase(
    user_repo: UserRepository = Depends(get_user_repo),
) -> GetUserUseCase:
    return GetUserUseCase(user_repository=user_repo)

def get_delete_user_usecase(
    user_repo: UserRepository = Depends(get_user_repo),
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_repository=user_repo)

def get_update_user_password_usecase(
    user_repo: UserRepository = Depends(get_user_repo),
    encryption_service: EncryptionService = Depends(get_encryption_service),
) -> UpdateUserPasswordUseCase:
    return UpdateUserPasswordUseCase(user_repository=user_repo, encryption_service=encryption_service)

def get_route_repo(
    session: AsyncSession = Depends(get_db_session),
) -> RouteRepository:
    return RouteRepository(session)



def get_bbox() -> BoundingBox:
    return BoundingBox(
        min_lat=config.geo.min_lat,
        min_lon=config.geo.min_lon,
        max_lat=config.geo.max_lat,
        max_lon=config.geo.max_lon,
    )


def get_coordinate_generator() -> CoordinateGeneratorService:
    return CoordinateGenerator()


def get_create_route_usecase(
    route_repo: RouteRepository = Depends(get_route_repo),
    osrm_client: OsrmClient = Depends(get_osrm_client),
) -> CreateRouteUseCase:
    return CreateRouteUseCase(osrm_client=osrm_client, route_repo=route_repo)


def get_route_by_id_usecase(
    route_repo: RouteRepository = Depends(get_route_repo),
) -> GetRouteByIdUseCase:
    return GetRouteByIdUseCase(route_repo=route_repo)


def get_route_metrics_usecase(
    osrm_client: OsrmClient = Depends(get_osrm_client),
) -> GetRouteMetricsUseCase:
    return GetRouteMetricsUseCase(osrm_client=osrm_client)


def get_delete_route_usecase(
    route_repo: RouteRepository = Depends(get_route_repo),
) -> DeleteRouteUseCase:
    return DeleteRouteUseCase(route_repo=route_repo)


def get_optimize_route_usecase(
    osrm_client: OsrmClient = Depends(get_osrm_client),
) -> OptimizeRouteUseCase:
    return OptimizeRouteUseCase(osrm_client=osrm_client)


def get_generate_random_coordinates_usecase(
    generator: CoordinateGenerator = Depends(get_coordinate_generator),
    bbox: BoundingBox = Depends(get_bbox),
) -> GenerateRandomCoordinatesUseCase:
    return GenerateRandomCoordinatesUseCase(generator=generator, bbox=bbox)
