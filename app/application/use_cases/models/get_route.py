from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class GetRouteInput:
    route_id: int

@dataclass(frozen=True, slots=True)
class GetRouteOutput:
    route_id: int
    user_id: int
    distance: float
    duration: float
    geometry: dict