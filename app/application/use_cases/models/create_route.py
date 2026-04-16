from dataclasses import dataclass

from app.domain.models.coordinate import Coordinate


@dataclass(frozen=True, slots=True)
class CreateRouteInput:
    user_id: int
    coords: list[Coordinate]
    profile: str = "driving"


@dataclass(frozen=True, slots=True)
class CreateRouteOutput:
    route_id: int
    user_id: int
    distance: float
    duration: float
    geometry: dict