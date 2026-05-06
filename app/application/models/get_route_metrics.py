from dataclasses import dataclass

from app.domain.models.coordinate import Coordinate


@dataclass(frozen=True, slots=True)
class GetRouteMetricsInput:
    coords: list[Coordinate]
    profile: str = "driving"


@dataclass(frozen=True, slots=True)
class GetRouteMetricsOutput:
    distance: float
    duration: float
    geometry: dict
