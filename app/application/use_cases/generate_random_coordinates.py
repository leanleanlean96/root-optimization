from app.domain.models.coordinate import BoundingBox
from app.domain.services.coordinate_generator_service import CoordinateGenerator

from .models.generate_random_coordinates import (
    GenerateRandomCoordinatesInput,
    GenerateRandomCoordinatesOutput,
)


class GenerateRandomCoordinatesUseCase:
    def __init__(
        self,
        generator: CoordinateGenerator,
        bbox: BoundingBox,
    ) -> None:
        self._generator = generator
        self._bbox = bbox

    async def execute(
        self, input: GenerateRandomCoordinatesInput
    ) -> GenerateRandomCoordinatesOutput:
        coords = self._generator.generate(input.count, self._bbox)
        return GenerateRandomCoordinatesOutput(coords=coords)