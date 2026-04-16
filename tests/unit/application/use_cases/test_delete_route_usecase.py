import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.delete_route import DeleteRouteUseCase
from app.application.use_cases.models.delete_user import DeleteRouteInput
from app.application.exceptions import RouteNotFoundException
from app.domain.models.route import RouteData, RouteMetrics

@pytest.mark.asyncio
async def test_delete_route_usecase_success():
    # 1. Подготовка
    route_id = 123
    input_data = DeleteRouteInput(route_id=route_id)

    # 2. Мок репозитория
    mock_repo = AsyncMock()
    fake_route = RouteData(
        id=route_id,
        user_id=1,
        metrics=RouteMetrics(distance=100, duration=50, geometry={})
    )
    mock_repo.get_route_by_id.return_value = fake_route
    mock_repo.delete_by_id.return_value = None  # заглушка

    # 3. Выполнение
    usecase = DeleteRouteUseCase(route_repo=mock_repo)
    await usecase.execute(input_data)

    # 4. Проверки
    mock_repo.get_route_by_id.assert_awaited_once_with(route_id)
    mock_repo.delete_by_id.assert_awaited_once_with(route_id)

@pytest.mark.asyncio
async def test_delete_route_usecase_not_found():
    route_id = 999
    input_data = DeleteRouteInput(route_id=route_id)

    mock_repo = AsyncMock()
    mock_repo.get_route_by_id.return_value = None  # маршрут не найден

    usecase = DeleteRouteUseCase(route_repo=mock_repo)
    with pytest.raises(RouteNotFoundException, match="Route not found"):
        await usecase.execute(input_data)

    mock_repo.delete_by_id.assert_not_awaited() 