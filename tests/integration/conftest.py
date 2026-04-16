import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def client():
    # Создаём мок-конфиг с нужными полями
    mock_config = Mock()
    
    # AppConfig
    mock_config.app = Mock()
    mock_config.app.name = "RootOptimization"
    mock_config.app.host = "0.0.0.0"
    mock_config.app.port = 8080
    
    # JwtConfig
    mock_config.jwt = Mock()
    mock_config.jwt.secret_key = "test_secret"
    mock_config.jwt.public_key = "test_public"
    mock_config.jwt.access_key_delta = 900  # 15 минут в секундах
    mock_config.jwt.refresh_key_delta = 172800  # 2 дня
    mock_config.jwt.algorithm = "HS256"
    
    # DbConfig
    mock_config.db = Mock()
    mock_config.db.url = "postgresql+asyncpg://test:test@localhost/test"
    mock_config.db.echo = False
    mock_config.db.echo_pool = False
    mock_config.db.pool_size = 25
    mock_config.db.max_overflow = 10
    mock_config.db.naming_convention = {}  # не важно
    
    # OsrmConfig
    mock_config.osrm = Mock()
    mock_config.osrm.url = "http://localhost:5000"
    
    # GeoConfig
    mock_config.geo = Mock()
    mock_config.geo.min_lat = 50.0
    mock_config.geo.min_lon = 30.0
    mock_config.geo.max_lat = 60.0
    mock_config.geo.max_lon = 40.0
    
    mock_config.debug = True
    mock_config.prefix = Mock()
    mock_config.prefix.prefix = "/api"
    
    # Патчим config в модуле app.core.config
    with patch('app.core.config.config', mock_config):
        from app.main import app
        yield TestClient(app)