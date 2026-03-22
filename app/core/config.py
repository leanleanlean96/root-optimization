from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    naming_convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class ApiPrefix(BaseModel):
    prefix: str = "/api"

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("app/env/.env", "app/env/.env.template"),
        env_ignore_empty=True,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    app: AppConfig = AppConfig()
    prefix: ApiPrefix = ApiPrefix()
    db: DbConfig
    debug: bool = False

config = Config()