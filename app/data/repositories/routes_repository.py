from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.models.route import RouteData, RouteMetrics

from ..schemas import Route

class RouteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_route(self, user_id: int, route_metrics: RouteMetrics) -> RouteData:
        db_route: Route = Route(
            user_id=user_id,
            distance_m=route_metrics.distance,
            duration_s=route_metrics.duration,
            geometry=route_metrics.geometry
        )
        self.session.add(db_route)
        await self.session.commit()
        await self.session.refresh(db_route)
        
        route_metrics = RouteMetrics(
            distance=db_route.distance_m,
            duration=db_route.duration_s,
            geometry=db_route.geometry,
        )

        return RouteData(
            id=db_route.id,
            user_id=db_route.user_id,
            metrics=route_metrics,
        )
    
    async def get_route_by_id(self, route_id: int) -> RouteData | None:
        query_result = await self.session.execute(
            select(Route).where(Route.id == route_id,
                                Route.is_deleted == False)
        )

        db_route = query_result.scalar_one_or_none()

        if db_route is None:
            return None
        
        route_metrics = RouteMetrics(
            distance=db_route.distance_m,
            duration=db_route.duration_s,
            geometry=db_route.geometry,
        )

        return RouteData(
            id=db_route.id,
            user_id=db_route.user_id,
            metrics=route_metrics,
        )
    
    async def get_routes_by_user_id(self, user_id: int) -> list[RouteData]:
        query_result = await self.session.execute(
            select(Route).where(Route.user_id == user_id,
                                Route.is_deleted == False)
        )

        user_routes = query_result.scalars().all()
        
        routes: list[RouteData] = []

        for db_route in user_routes:
            route_metrics = RouteMetrics(
                distance=db_route.distance_m,
                duration=db_route.duration_s,
                geometry=db_route.geometry,
            )

            routes.append(RouteData(
                id=db_route.id,
                user_id=db_route.user_id,
                metrics=route_metrics,
            ))

        return routes
    
    async def delete_by_id(self, route_id: int) -> None:
        route = await self.get_route_by_id(route_id=route_id)

        if route:
            route.is_deleted = True
            await self.session.commit()