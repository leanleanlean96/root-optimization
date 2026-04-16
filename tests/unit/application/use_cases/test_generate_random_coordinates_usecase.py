import pytest
from unittest.mock import Mock
from app.application.use_cases.generate_random_coordinates import GenerateRandomCoordinatesUseCase
from app.application.use_cases.models.generate_random_coordinates import GenerateRandomCoordinatesInput
from app.domain.models.coordinate import BoundingBox, Coordinate

@pytest.fixture
def mock_generator():
    generator = Mock()
    # По умолчанию возвращаем список из 3 фейковых координат
    def generate_side_effect(count, bbox):
        return [Coordinate(lat=55.0 + i, lon=37.0 + i) for i in range(count)]
    generator.generate.side_effect = generate_side_effect
    return generator

@pytest.fixture
def mock_bbox():
    return BoundingBox(min_lat=50.0, max_lat=60.0, min_lon=30.0, max_lon=40.0)

@pytest.mark.asyncio
async def test_generate_random_coordinates_returns_correct_count(mock_generator, mock_bbox):
    usecase = GenerateRandomCoordinatesUseCase(generator=mock_generator, bbox=mock_bbox)
    count = 5
    input_data = GenerateRandomCoordinatesInput(count=count)
    result = await usecase.execute(input_data)

    assert len(result.coords) == count
    mock_generator.generate.assert_called_once_with(count, mock_bbox)

@pytest.mark.asyncio
async def test_generate_random_coordinates_default_count(mock_generator, mock_bbox):
    usecase = GenerateRandomCoordinatesUseCase(generator=mock_generator, bbox=mock_bbox)
    # Предполагаем, что в Input значение по умолчанию count=10 (или другое). 
    # Если нет значения по умолчанию, укажем явно, например count=10.
    input_data = GenerateRandomCoordinatesInput(count=10)
    result = await usecase.execute(input_data)

    assert len(result.coords) == 10
    mock_generator.generate.assert_called_once_with(10, mock_bbox)