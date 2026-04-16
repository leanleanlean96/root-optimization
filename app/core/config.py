from datetime import timedelta
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import ClassVar


class AppConfig(BaseModel):
    name: str = "RootOptimization"
    host: str = "0.0.0.0"
    port: int = 8080


class JwtConfig(BaseModel):
    secret_key: str
    public_key: str
    access_key_delta: timedelta = timedelta(minutes=15)
    refresh_key_delta: timedelta = timedelta(days=2)
    algorithm: str


class DbConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 25
    max_overflow: int = 10

    naming_convention: ClassVar[dict[str, str]] = {
        "ix": "ix__%(table_name)s__%(column_0_name)s",
        "uq": "uq__%(table_name)s__%(column_0_name)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
        "fk": "fk__%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
        "pk": "pk__%(table_name)s",
    }


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class OsrmConfig(BaseModel):
    url: str


class GeoConfig(BaseModel):
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        env_ignore_empty=True,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    app: AppConfig = AppConfig()
    prefix: ApiPrefix = ApiPrefix()
    db: DbConfig
    jwt: JwtConfig
    osrm: OsrmConfig
    geo: GeoConfig
    debug: bool = False


config = Config()
