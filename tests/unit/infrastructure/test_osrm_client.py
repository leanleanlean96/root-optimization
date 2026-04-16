import pytest
from unittest.mock import AsyncMock, Mock, patch
import httpx
from app.infrastructure.osrm_client import OsrmClient
from app.domain.models.coordinate import Coordinate
from app.infrastructure.exceptions import OsrmServiceException, OsrmServiceUnavailableException

@pytest.fixture
def mock_async_client():
    return AsyncMock(spec=httpx.AsyncClient)

@pytest.fixture
def osrm_client(mock_async_client):
    return OsrmClient(service_url="http://osrm:5000", client=mock_async_client)

@pytest.mark.asyncio
async def test_get_route_metrics_success(osrm_client, mock_async_client):
    coords = [Coordinate(lat=55.751, lon=37.618), Coordinate(lat=55.752, lon=37.619)]
    
    # Создаём синхронный мок для ответа
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "code": "Ok",
        "routes": [{"distance": 1000, "duration": 120, "geometry": {"type": "LineString", "coordinates": []}}]
    }
    mock_async_client.get.return_value = mock_response

    result = await osrm_client.get_route_metrics(coords, "driving")

    expected_url = "http://osrm:5000/route/v1/driving/37.618,55.751;37.619,55.752"
    mock_async_client.get.assert_called_once_with(
        expected_url,
        params={"geometries": "geojson", "overview": "full"},
        timeout=30.0
    )
    assert result.distance == 1000
    assert result.duration == 120
    assert result.geometry == {"type": "LineString", "coordinates": []}

@pytest.mark.asyncio
async def test_get_route_metrics_timeout(osrm_client, mock_async_client):
    coords = [Coordinate(lat=55.751, lon=37.618)]
    mock_async_client.get.side_effect = httpx.TimeoutException("Timeout")
    with pytest.raises(OsrmServiceUnavailableException, match="OSRM service timed out"):
        await osrm_client.get_route_metrics(coords)

@pytest.mark.asyncio
async def test_get_route_metrics_connect_error(osrm_client, mock_async_client):
    coords = [Coordinate(lat=55.751, lon=37.618)]
    mock_async_client.get.side_effect = httpx.ConnectError("Can't connect")
    with pytest.raises(OsrmServiceUnavailableException, match="OSRM service is unavailable"):
        await osrm_client.get_route_metrics(coords)

@pytest.mark.asyncio
async def test_get_route_metrics_osrm_error_code(osrm_client, mock_async_client):
    coords = [Coordinate(lat=55.751, lon=37.618)]
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"code": "NoRoute", "message": "No route found"}
    mock_async_client.get.return_value = mock_response
    with pytest.raises(OsrmServiceException, match="OSRM error: No route found"):
        await osrm_client.get_route_metrics(coords)

@pytest.mark.asyncio
async def test_optimize_route_success(osrm_client, mock_async_client):
    coords = [
        Coordinate(lat=55.751, lon=37.618),
        Coordinate(lat=55.752, lon=37.619),
        Coordinate(lat=55.753, lon=37.620)
    ]
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "code": "Ok",
        "trips": [{"distance": 500, "duration": 60, "geometry": {"type": "LineString", "coordinates": []}}]
    }
    mock_async_client.get.return_value = mock_response

    result = await osrm_client.optimize_route(coords, "driving")

    expected_url = "http://osrm:5000/trip/v1/driving/37.618,55.751;37.619,55.752;37.62,55.753"
    mock_async_client.get.assert_called_once_with(
        expected_url,
        params={
            "roundtrip": "true",
            "source": "first",
            "destination": "any",
            "steps": "false",
            "geometries": "geojson",
            "overview": "full",
        },
        timeout=30.0
    )
    assert result.distance == 500
    assert result.duration == 60

@pytest.mark.asyncio
async def test_optimize_route_http_error(osrm_client, mock_async_client):
    coords = [Coordinate(lat=55.751, lon=37.618)]
    # Создаём реальный HTTPStatusError с подходящим response
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    error = httpx.HTTPStatusError("500", request=Mock(), response=mock_response)
    mock_async_client.get.side_effect = error

    with pytest.raises(OsrmServiceException, match="OSRM returned 500: Internal Server Error"):
        await osrm_client.optimize_route(coords)