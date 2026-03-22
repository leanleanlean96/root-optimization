from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from core.config import config

from data.dbclient import db_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shutdown
    await db_client.dispose()

main_app = FastAPI(
    title=config.app.name,
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=config.app.host,
        port=config.app.port,
        reload=True,
    )