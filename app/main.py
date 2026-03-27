from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from app.api.routes.routes import router as routes_router

from app.core.config import config

from app.data.dbclient import db_client


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

main_app.include_router(routes_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=config.app.host,
        port=config.app.port,
        reload=True,
    )
