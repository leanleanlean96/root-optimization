from infrastructure.osrm_client import OsrmClient
from data.repositories.routes_repository import RouteRepository
from domain.models.route import RouteData, RouteMetrics
from .models.create_route import CreateRouteInput, CreateRouteOutput

class CreateRouteUseCase:
    def __init__(self, osrm_client: OsrmClient, route_repo: RouteRepository):
        self.osrm_client = osrm_client
        self.route_repo = route_repo

    async def execute(self, input: CreateRouteInput) -> CreateRouteOutput:
        metrics: RouteMetrics = await self.osrm_client.get_route_metrics(
            dots=input.coords,
            profile=input.profile,
        )
        route: RouteData = await self.route_repo.create_route(input.user_id, metrics)
        return CreateRouteOutput(
            route_id=route.id,
            user_id=route.user_id,
            distance=route.metrics.distance,
            duration=route.metrics.duration,
            geometry=route.metrics.geometry,
        )