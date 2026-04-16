from typing import Protocol

from ..models.coordinate import BoundingBox, Coordinate


class CoordinateGenerator(Protocol):
    def generate(self, count: int, bbox: BoundingBox) -> list[Coordinate]:
        """Return `count` points, all inside `bbox`."""
        ...
