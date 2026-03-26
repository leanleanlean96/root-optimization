from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class RouteMetrics:
    distance: float
    duration: float
    geometry: Any


@dataclass(frozen=True, slots=True)
class RouteData:
    id: int | None
    user_id: int
    metrics: RouteMetrics
