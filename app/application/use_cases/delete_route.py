from app.domain.repositories.route_repo import RouteRepository
from app.domain.models.route import RouteData

from .models.delete_user import DeleteRouteInput
from ..exceptions import RouteNotFoundException

class DeleteRouteUseCase:
    def __init__(self, route_repo: RouteRepository):
        self.route_repo = route_repo

    async def execute(self, input: DeleteRouteInput) -> None:
        route: RouteData = await self.route_repo.get_route_by_id(input.route_id)
        if route is None:
            raise RouteNotFoundException("Route not found")

        await self.route_repo.delete_by_id(input.route_id)
