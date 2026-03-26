from data.repositories.routes_repository import RouteRepository
from domain.models.route import RouteData

from .models.get_route import GetRouteInput, GetRouteOutput

class GetRouteById:
    def __init__(self, route_repo: RouteRepository):
        self.route_repo = route_repo

    async def execute(self, input: GetRouteInput) -> GetRouteOutput:
        route: RouteData | None = await self.route_repo.get_route_by_id(GetRouteInput.route_id)
        if route is None:
            #TODO: Write custom exceptions
            raise ValueError("Route not found")
        
        output: GetRouteOutput = GetRouteOutput(
            route_id=route.id,
            user_id=route.user_id,
            distance=route.metrics.distance,
            duration=route.metrics.duration,
            geometry=route.metrics.geometry
        )
        
        return output