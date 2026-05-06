from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import AsyncClient
import uvicorn
from app.api.routes.routes import router as routes_router
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.core.config import config
from app.data.dbclient import DbClient
from app.application.exceptions import RouteNotFoundException
from app.infrastructure.exceptions import (
    OsrmServiceException,
    OsrmServiceUnavailableException,
)
from app.core.exceptions import UnauthorizedException

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    db_client = DbClient(
        url=str(config.db.url),
        echo=config.db.echo,
        echo_pool=config.db.echo_pool,
        pool_size=config.db.pool_size,
        max_overflow=config.db.max_overflow,
    )

    app.state.db_client = db_client

    http_client = AsyncClient(timeout=30.0)
    app.state.http_client = http_client
    yield
    # shutdown
    await app.state.http_client.aclose()
    await app.state.db_client.dispose()

main_app = FastAPI(
    title=config.app.name,
    lifespan=lifespan,
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.app.frontend_url],
    allow_methods=["*"],
    allow_headers=["*"],
)

@main_app.exception_handler(RouteNotFoundException)
async def unicorn_route_not_found_handler(request: Request, exc: RouteNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": "Route Not Found"},
    )
@main_app.exception_handler(OsrmServiceUnavailableException)
async def unicorn_osrm_service_unavailable_handler(
    request: Request, exc: OsrmServiceUnavailableException
):
    return JSONResponse(
        status_code=503,
        content={"message": "Route Service Unavailable"},
    )
@main_app.exception_handler(OsrmServiceException)
async def unicorn_osrm_service_exception_handler(request: Request, exc: OsrmServiceException):
    return JSONResponse(
        status_code=500,
        content={"message": "Something Unusual Happened"},
    )
@main_app.unauthorized_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})

main_app.include_router(routes_router, prefix=config.prefix.prefix)
main_app.include_router(users_router, prefix=config.prefix.prefix)
main_app.include_router(auth_router, prefix=config.prefix.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=config.app.host,
        port=config.app.port,
        reload=True,
    )