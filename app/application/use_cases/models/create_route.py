from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateRouteInput:
    user_id: int
    coords: list[tuple[float, float]]
    profile: str = "driving"


@dataclass(frozen=True, slots=True)
class CreateRouteOutput:
    route_id: int
    user_id: int
    distance: float
    duration: float
    geometry: dict
