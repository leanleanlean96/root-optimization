from dataclasses import dataclass

from app.domain.models.coordinate import Coordinate


@dataclass(frozen=True, slots=True)
class GenerateRandomCoordinatesInput:
    count: int


@dataclass(frozen=True, slots=True)
class GenerateRandomCoordinatesOutput:
    coords: list[Coordinate]