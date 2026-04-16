from typing import Protocol

from ..models.coordinate import Coordinate
from ..models.route import RouteMetrics


class OsrmService(Protocol):
    async def get_route_metrics(
        self, dots: list[Coordinate], profile: str
    ) -> RouteMetrics:
        ...

    async def optimize_route(
        self, dots: list[Coordinate], profile: str
    ) -> RouteMetrics:
        ...