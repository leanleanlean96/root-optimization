from typing import Protocol, Tuple

from ..models.route import RouteMetrics

class OsrmService(Protocol):
    async def get_route_metrics(
        self, dots: list[Tuple[float, float]], profile: str
    ) -> RouteMetrics:
        ...