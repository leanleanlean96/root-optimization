from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Coordinate:
    lat: float
    lon: float

    def __post_init__(self) -> None:
        if not -90.0 <= self.lat <= 90.0:
            raise ValueError(f"Invalid latitude: {self.lat}")
        if not -180.0 <= self.lon <= 180.0:
            raise ValueError(f"Invalid longitude: {self.lon}")


@dataclass(frozen=True, slots=True, kw_only=True)
class BoundingBox:
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float

    def __post_init__(self) -> None:
        if not (-90.0 <= self.min_lat <= self.max_lat <= 90.0):
            raise ValueError("Invalid latitude bounds")
        if not (-180.0 <= self.min_lon <= self.max_lon <= 180.0):
            raise ValueError("Invalid longitude bounds")

    @property
    def width(self) -> float:
        return self.max_lon - self.min_lon

    @property
    def height(self) -> float:
        return self.max_lat - self.min_lat

    def contains(self, point: Coordinate) -> bool:
        return (
            self.min_lon <= point.lon <= self.max_lon
            and self.min_lat <= point.lat <= self.max_lat
        )
