from app.data.repositories.routes_repository import RouteRepository
from app.domain.models.route import RouteData

from .models.delete_user import DeleteRouteInput

class DeleteRouteUseCase:
    def __init__(self, route_repo: RouteRepository):
        self.route_repo = route_repo

    async def execute(self, input: DeleteRouteInput) -> None:
        route: RouteData = await self.route_repo.get_route_by_id(input.route_id)
        if route is None:
            #TODO: Write custom exceptions
            raise ValueError("User not found")

        await self.route_repo.delete_by_id(input.route_id)