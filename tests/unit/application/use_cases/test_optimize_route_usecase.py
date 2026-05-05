import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.optimize_route import OptimizeRouteUseCase
from app.application.use_cases.models.get_route_metrics import GetRouteMetricsInput, GetRouteMetricsOutput
from app.domain.models.coordinate import Coordinate
from app.domain.models.route import RouteMetrics

@pytest.mark.asyncio
async def test_optimize_route_usecase():
    mock_osrm = AsyncMock()
    fake_route = RouteMetrics(distance=200, duration=100, geometry={"type": "LineString"})
    mock_osrm.optimize_route.return_value = fake_route

    usecase = OptimizeRouteUseCase(osrm_client=mock_osrm)
    coords = [Coordinate(lat=55.751, lon=37.618), Coordinate(lat=55.753, lon=37.620)]
    input_data = GetRouteMetricsInput(coords=coords, profile="car")

    result = await usecase.execute(input_data)

    mock_osrm.optimize_route.assert_called_once_with(coords, "car")
    assert result.distance == 200
    assert result.duration == 100