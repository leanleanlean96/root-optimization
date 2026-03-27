from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from core.config import config

from data.dbclient import db_client

from api.routes.users import router



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
main_app.include_router(router, prefix=config.prefix.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=config.app.host,
        port=config.app.port,
        reload=True,
    )
