from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.data.dbclient import db_client
from app.data.repositories.routes_repository import RouteRepository
from app.infrastructure.osrm_client import OsrmClient
from app.application.use_cases.create_route import CreateRouteUseCase
from app.application.use_cases.get_route import GetRouteByIdUseCase
from app.application.use_cases.get_route_metrics import GetRouteMetricsUseCase
from app.application.use_cases.delete_route import DeleteRouteUseCase

from app.core.config import config

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_client.session_getter():
        yield session

async def get_http_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(timeout=30.0) as client:
        yield client

def get_osrm_client(service_url: str = config.osrm.url, client: AsyncClient = Depends(get_http_client)) -> OsrmClient:
    return OsrmClient(service_url, client)

def get_route_repo(
    session: AsyncSession = Depends(get_db_session),
) -> RouteRepository:
    return RouteRepository(session)

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
    osrm_client: OsrmClient = Depends(get_osrm_client)
) -> GetRouteMetricsUseCase:
    return GetRouteMetricsUseCase(osrm_client=osrm_client)

def get_delete_route_usecase(
    route_repo: RouteRepository = Depends(get_route_repo),
) -> DeleteRouteUseCase:
    return DeleteRouteUseCase(route_repo=route_repo)