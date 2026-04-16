import math
import random

from app.domain.models.coordinate import BoundingBox, Coordinate


class CoordinateGenerator:
    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def generate(self, count: int, bbox: BoundingBox) -> list[Coordinate]:
        if count <= 0:
            return []

        cols, rows = self._grid_shape(count, bbox)
        cells = [(c, r) for r in range(rows) for c in range(cols)]
        self._rng.shuffle(cells)

        cell_w = bbox.width / cols
        cell_h = bbox.height / rows

        result: list[Coordinate] = []
        for c, r in cells[:count]:
            lon = bbox.min_lon + (c + self._rng.random()) * cell_w
            lat = bbox.min_lat + (r + self._rng.random()) * cell_h
            result.append(Coordinate(lat=lat, lon=lon))
        return result

    @staticmethod
    def _grid_shape(count: int, bbox: BoundingBox) -> tuple[int, int]:
        aspect = bbox.width / bbox.height if bbox.height > 0 else 1.0
        rows = max(1, int(math.sqrt(count / aspect)))
        cols = max(1, math.ceil(count / rows))
        while cols * rows < count:
            cols += 1
        return cols, rows
