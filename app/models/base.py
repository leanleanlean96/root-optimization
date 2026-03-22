from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from core.config import config

class Base(DeclarativeBase):
    metadata: MetaData = MetaData(
        naming_convention=config.db.naming_convention,
    )
    pass


