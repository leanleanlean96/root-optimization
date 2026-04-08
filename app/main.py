from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import uvicorn

from fastapi import FastAPI

from app.api.routes.routes import router as routes_router

from app.core.config import config

from app.data.dbclient import db_client

from app.application.exceptions import RouteNotFoundException
from app.infrastructure.exceptions import OsrmServiceException, OsrmServiceUnavailableException
from app.core.exceptions import UnauthorizedException


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_client.dispose()


main_app = FastAPI(
    title=config.app.name,
    lifespan=lifespan,
)

@main_app.exception_handler(RouteNotFoundException)
async def unicorn_exception_handler(request: Request, exc: RouteNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Route Not Found"},
    )

@main_app.exception_handler(RouteNotFoundException)
async def unicorn_exception_handler(request: Request, exc: OsrmServiceUnavailableException):
    return JSONResponse(
        status_code=503,
        content={"message": f"Route Service Unavailable"},
    )

@main_app.exception_handler(RouteNotFoundException)
async def unicorn_exception_handler(request: Request, exc: OsrmServiceException):
    return JSONResponse(
        status_code=500,
        content={"message": f"Something Unusual Happened"},
    )

@main_app.exception_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(status_code=401, content={"Unauthorized"})

main_app.include_router(routes_router, prefix=config.prefix.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=config.app.host,
        port=config.app.port,
        reload=True,
    )
