from dataclasses import dataclass
from typing import Any

GeoJson = dict[str, Any]

@dataclass(frozen=True, slots=True)
class RouteMetrics:
    distance: float
    duration: float
    geometry: GeoJson


@dataclass(frozen=True, slots=True)
class RouteData:
    id: int | None
    user_id: int
    metrics: RouteMetrics
