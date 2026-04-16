from fastapi import Depends, Header
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.core.auth.auth_service import JwtAuthService
from app.core.auth.models import UserClaims
from app.core.config import config
from app.data.dbclient import db_client
from app.data.repositories.routes_repository import RouteRepository
from app.infrastructure.osrm_client import OsrmClient
from app.application.use_cases.create_route import CreateRouteUseCase
from app.application.use_cases.delete_route import DeleteRouteUseCase
from app.application.use_cases.generate_random_coordinates import (
    GenerateRandomCoordinatesUseCase,
)
from app.application.use_cases.get_route import GetRouteByIdUseCase
from app.application.use_cases.get_route_metrics import GetRouteMetricsUseCase
from app.application.use_cases.optimize_route import OptimizeRouteUseCase
from app.core.auth.auth_service import JwtAuthService
from app.core.auth.models import UserClaims
from app.core.config import config
from app.core.exceptions import (
    InvalidTokenException,
    InvalidTokenTypeException,
    TokenExpiredException,
    UnauthorizedException,
)
from app.data.dbclient import db_client
from app.data.repositories.routes_repository import RouteRepository
from app.domain.models.coordinate import BoundingBox
from app.domain.services.coordinate_generator_service import CoordinateGenerator
from app.infrastructure.coordinate_generator import (
    CoordinateGenerator,
)
from app.infrastructure.osrm_client import OsrmClient


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_client.session_getter():
        yield session


async def get_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(timeout=30.0) as client:
        yield client


def get_auth_service() -> JwtAuthService:
    return JwtAuthService(
        secret=config.jwt.secret_key,
        access_timedelta=config.jwt.access_key_delta,
        refresh_timedelta=config.jwt.refresh_key_delta,
        algorithm=config.jwt.algorithm,
    )


async def get_user_claims(
    auth_string: str = Header(...),
    auth_service: JwtAuthService = Depends(get_auth_service),
) -> UserClaims:
    try:
        token = auth_string.removeprefix("Bearer ")
        return auth_service.get_payload_data(token)
    # TODO: add custom JWTservice exceptions
    except (
        TokenExpiredException,
        InvalidTokenException,
        InvalidTokenTypeException,
    ) as e:
        raise UnauthorizedException(f"Unauthorized: {e}")


def get_auth_service() -> JwtAuthService:
    return JwtAuthService(
        secret=config.jwt.secret_key,
        access_timedelta=config.jwt.access_key_delta,
        refresh_timedelta=config.jwt.refresh_key_delta,
        algorithm=config.jwt.algorithm,
    )


async def get_user_claims(
    auth_string: str = Header(...),
    auth_service: JwtAuthService = Depends(get_auth_service),
) -> UserClaims:
    try:
        token = auth_string.removeprefix("Bearer ")
        return auth_service.get_payload_data(token)
    except (
        TokenExpiredException,
        InvalidTokenException,
        InvalidTokenTypeException,
    ) as e:
        raise UnauthorizedException(f"Unauthorized: {e}")


def get_osrm_client(
    service_url: str = config.osrm.url,
    client: AsyncClient = Depends(get_http_client),
) -> OsrmClient:
    return OsrmClient(service_url, client)


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


def get_coordinate_generator() -> CoordinateGenerator:
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
