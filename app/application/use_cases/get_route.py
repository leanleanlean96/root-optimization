from app.domain.repositories.route_repo import RouteRepository
from app.domain.models.route import RouteData

from .models.get_route import GetRouteInput, GetRouteOutput
from ..exceptions import RouteNotFoundException


class GetRouteByIdUseCase:
    def __init__(self, route_repo: RouteRepository):
        self.route_repo = route_repo

    async def execute(self, input: GetRouteInput) -> GetRouteOutput:
        route: RouteData | None = await self.route_repo.get_route_by_id(input.route_id)
        if route is None:
            raise RouteNotFoundException(f"Route with id {input.route_id} not found")

        output: GetRouteOutput = GetRouteOutput(
            route_id=route.id,
            user_id=route.user_id,
            distance=route.metrics.distance,
            duration=route.metrics.duration,
            geometry=route.metrics.geometry,
        )

        return output


# TODO: get all routes for user
