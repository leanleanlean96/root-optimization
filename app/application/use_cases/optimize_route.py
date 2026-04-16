from app.domain.models.route import RouteMetrics
from app.domain.services.osrm_service import OsrmService

from .models.get_route_metrics import GetRouteMetricsInput, GetRouteMetricsOutput


class OptimizeRouteUseCase:
    def __init__(self, osrm_client: OsrmService):
        self.osrm_client = osrm_client

    async def execute(self, input: GetRouteMetricsInput) -> GetRouteMetricsOutput:
        route: RouteMetrics = await self.osrm_client.optimize_route(
            input.coords, input.profile
        )

        output: GetRouteMetricsOutput = GetRouteMetricsOutput(
            distance=route.distance, duration=route.duration, geometry=route.geometry
        )

        return output
