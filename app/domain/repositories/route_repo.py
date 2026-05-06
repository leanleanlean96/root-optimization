from typing import Protocol

from ..models.route import RouteData, RouteMetrics


class RouteRepository(Protocol):
    async def create_route(
        self, user_id: int, route_metrics: RouteMetrics
    ) -> RouteData: ...
    
    async def delete_by_id(self, route_id: int) -> None: ...

    async def get_route_by_id(self, route_id: int) -> RouteData | None: ...

    async def get_routes_by_user_id(self, user_id: int, offset: int, limit: int) -> list[RouteData]: ...

    async def delete_by_id(self, route_id: int) -> None: ...
