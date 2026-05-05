import os
import pytest
from fastapi.testclient import TestClient

os.environ["APP_CONFIG__DB__URL"] = "postgresql+asyncpg://postgres:postgres@db:5432/delivery_db"
os.environ["APP_CONFIG__JWT__SECRET_KEY"] = "test_secret_key"
os.environ["APP_CONFIG__JWT__PUBLIC_KEY"] = "test_public_key"
os.environ["APP_CONFIG__JWT__ALGORITHM"] = "HS256"
os.environ["APP_CONFIG__OSRM__URL"] = "http://localhost:5000"
os.environ["APP_CONFIG__GEO__MIN_LAT"] = "50.0"
os.environ["APP_CONFIG__GEO__MAX_LAT"] = "60.0"
os.environ["APP_CONFIG__GEO__MIN_LON"] = "30.0"
os.environ["APP_CONFIG__GEO__MAX_LON"] = "40.0"
os.environ["APP_CONFIG__DEBUG"] = "true"

for old_var in ["postgres_user", "postgres_password", "postgres_db", "postgres_host", "postgres_port", "backend_port", "osrm_url"]:
    os.environ.pop(old_var, None)

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)