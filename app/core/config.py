from pydantic import BaseModel
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import ClassVar


class AppConfig(BaseModel):
    name: str = "RootOptimization"
    host: str = "0.0.0.0"
    port: int = 8080


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

class JWTConfig(BaseModel):
    secret_key: str = Field(default="your-super-secret-key-change-in-production", min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("app/env/.env.template", "app/env/.env"),
        env_ignore_empty=True,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    app: AppConfig = AppConfig()
    prefix: ApiPrefix = ApiPrefix()
    db: DbConfig
    jwt: JWTConfig = JWTConfig()
    debug: bool = False


config = Config()
