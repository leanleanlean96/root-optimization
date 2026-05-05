import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.get_route_metrics import GetRouteMetricsUseCase
from app.application.use_cases.models.get_route_metrics import GetRouteMetricsInput, GetRouteMetricsOutput
from app.domain.models.coordinate import Coordinate
from app.domain.models.route import RouteMetrics

@pytest.mark.asyncio
async def test_get_route_metrics_usecase():
    mock_osrm = AsyncMock()
    fake_route = RouteMetrics(distance=123.4, duration=56.7, geometry={"type": "LineString"})
    mock_osrm.get_route_metrics.return_value = fake_route

    usecase = GetRouteMetricsUseCase(osrm_client=mock_osrm)
    coords = [Coordinate(lat=55.751, lon=37.618), Coordinate(lat=55.752, lon=37.619)]
    input_data = GetRouteMetricsInput(coords=coords, profile="driving")

    result = await usecase.execute(input_data)

    mock_osrm.get_route_metrics.assert_called_once_with(coords, "driving")
    assert isinstance(result, GetRouteMetricsOutput)
    assert result.distance == 123.4
    assert result.duration == 56.7
    assert result.geometry == {"type": "LineString"}