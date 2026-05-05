import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.core.dependencies import (
    get_route_metrics_usecase,
    get_optimize_route_usecase,
    get_create_route_usecase,
    get_route_by_id_usecase,
    get_generate_random_coordinates_usecase,
)
from app.application.use_cases.models.get_route_metrics import GetRouteMetricsOutput
from app.application.use_cases.models.create_route import CreateRouteOutput
from app.application.use_cases.models.get_route import GetRouteOutput
from app.application.use_cases.models.generate_random_coordinates import GenerateRandomCoordinatesOutput
from app.domain.models.coordinate import Coordinate

@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


def test_post_route_metrics_success(client):
    from app.main import app
    mock_usecase = AsyncMock()
    mock_usecase.execute.return_value = GetRouteMetricsOutput(
        distance=1234.5,
        duration=678.9,
        geometry={"type": "LineString", "coordinates": [[37.618,55.751],[37.619,55.752]]}
    )
    app.dependency_overrides[get_route_metrics_usecase] = lambda: mock_usecase

    response = client.post("/routes/metrics", json={
        "coords": [{"lat": 55.751, "lon": 37.618}, {"lat": 55.752, "lon": 37.619}],
        "profile": "driving"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["distance"] == 1234.5
    assert data["duration"] == 678.9
    app.dependency_overrides.clear()


def test_post_route_optimize_success(client):
    mock_usecase = AsyncMock()
    mock_usecase.execute.return_value = GetRouteMetricsOutput(
        distance=500,
        duration=60,
        geometry={"type": "LineString", "coordinates": [[37.618,55.751],[37.620,55.753]]}
    )
    app.dependency_overrides[get_optimize_route_usecase] = lambda: mock_usecase

    response = client.post("/routes/optimize", json={
        "coords": [{"lat": 55.751, "lon": 37.618}, {"lat": 55.753, "lon": 37.620}],
        "profile": "driving"
    })
    assert response.status_code == 200
    assert response.json()["distance"] == 500
    app.dependency_overrides.clear()

def test_post_create_route_success(client):
    mock_usecase = AsyncMock()
    mock_usecase.execute.return_value = CreateRouteOutput(
        route_id=42,
        user_id=1,
        distance=1000,
        duration=120,
        geometry={"type": "LineString", "coordinates": []}
    )
    app.dependency_overrides[get_create_route_usecase] = lambda: mock_usecase

    response = client.post("/routes/create", json={
        "user_id": 1,
        "dots": [{"lat": 55.751, "lon": 37.618}],
        "profile": "driving"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["route_id"] == 42
    assert data["user_id"] == 1
    app.dependency_overrides.clear()

def test_post_create_route_empty_dots(client):
    response = client.post("/routes/create", json={
        "user_id": 1,
        "dots": [],
        "profile": "driving"
    })
    assert response.status_code == 422

def test_get_route_by_id_success(client):
    mock_usecase = AsyncMock()
    mock_usecase.execute.return_value = GetRouteOutput(
        route_id=10,
        user_id=2,
        distance=2000,
        duration=300,
        geometry={"type": "LineString", "coordinates": []}
    )
    app.dependency_overrides[get_route_by_id_usecase] = lambda: mock_usecase

    response = client.get("/routes/10")
    assert response.status_code == 200
    data = response.json()
    assert data["route_id"] == 10
    assert data["user_id"] == 2
    app.dependency_overrides.clear()

def test_post_random_coordinates_success(client):
    mock_usecase = AsyncMock()
    mock_usecase.execute.return_value = GenerateRandomCoordinatesOutput(
        coords=[Coordinate(lat=55.75, lon=37.62), Coordinate(lat=55.76, lon=37.63)]
    )
    app.dependency_overrides[get_generate_random_coordinates_usecase] = lambda: mock_usecase

    response = client.post("/routes/random-coordinates", json={"count": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["coords"]) == 2
    app.dependency_overrides.clear()

def test_post_random_coordinates_invalid_count(client):
    response = client.post("/routes/random-coordinates", json={"count": -1})
    assert response.status_code == 422