from sqlalchemy.ext.asyncio import AsyncSession
from data.dbclient import db_client


async def get_session():
    async for session in db_client.session_getter():
        yield session