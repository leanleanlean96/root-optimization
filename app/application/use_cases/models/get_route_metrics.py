from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class GetRouteMetricsInput:
    coords: list[tuple[float, float]]
    profile: str = "driving"

@dataclass(frozen=True, slots=True)
class GetRouteMetricsOutput:
    distance: float
    duration: float
    geometry: dict