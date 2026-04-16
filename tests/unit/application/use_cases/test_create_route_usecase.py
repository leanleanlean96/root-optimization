import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.create_route import CreateRouteUseCase
from app.application.use_cases.models.create_route import CreateRouteInput, CreateRouteOutput
from app.domain.models.coordinate import Coordinate
from app.domain.models.route import RouteMetrics, RouteData

@pytest.mark.asyncio
async def test_create_route_usecase_success():
    # 1. Подготовка данных
    coords = [Coordinate(lat=55.751, lon=37.618), Coordinate(lat=55.752, lon=37.619)]
    profile = "driving"
    user_id = 42
    input_data = CreateRouteInput(user_id=user_id, coords=coords, profile=profile)

    # 2. Мок OsrmService
    mock_osrm = AsyncMock()
    fake_metrics = RouteMetrics(
        distance=1234.5,
        duration=678.9,
        geometry={"type": "LineString", "coordinates": [[37.618,55.751],[37.619,55.752]]}
    )
    mock_osrm.get_route_metrics.return_value = fake_metrics

    # 3. Мок RouteRepository
    mock_repo = AsyncMock()
    fake_route_data = RouteData(
        id=1,
        user_id=user_id,
        metrics=fake_metrics
    )
    mock_repo.create_route.return_value = fake_route_data

    # 4. Выполнение usecase
    usecase = CreateRouteUseCase(osrm_client=mock_osrm, route_repo=mock_repo)
    result = await usecase.execute(input_data)

    # 5. Проверки
    mock_osrm.get_route_metrics.assert_awaited_once_with(dots=coords, profile=profile)
    mock_repo.create_route.assert_awaited_once_with(user_id, fake_metrics)
    assert isinstance(result, CreateRouteOutput)
    assert result.route_id == 1
    assert result.user_id == user_id
    assert result.distance == fake_metrics.distance
    assert result.duration == fake_metrics.duration
    assert result.geometry == fake_metrics.geometry

@pytest.mark.asyncio
async def test_create_route_usecase_osrm_error():
    coords = [Coordinate(lat=55.751, lon=37.618)]
    input_data = CreateRouteInput(user_id=1, coords=coords, profile="car")

    mock_osrm = AsyncMock()
    mock_osrm.get_route_metrics.side_effect = Exception("OSRM service error")
    mock_repo = AsyncMock()

    usecase = CreateRouteUseCase(osrm_client=mock_osrm, route_repo=mock_repo)
    with pytest.raises(Exception, match="OSRM service error"):
        await usecase.execute(input_data)

    mock_repo.create_route.assert_not_awaited() 