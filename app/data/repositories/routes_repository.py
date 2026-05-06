import json

from geoalchemy2.shape import from_shape, to_shape
from shapely import to_geojson
from shapely.geometry import shape
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.route import RouteData, RouteMetrics

from ..schemas import Route


class RouteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_route(
        self, user_id: int, route_metrics: RouteMetrics
    ) -> RouteData:
        db_route: Route = Route(
            user_id=user_id,
            distance_m=route_metrics.distance,
            duration_s=route_metrics.duration,
            geometry=from_shape(shape(route_metrics.geometry), srid=4326),
        )
        self.session.add(db_route)
        await self.session.commit()
        await self.session.refresh(db_route)

        return RouteData(
            id=db_route.id, user_id=db_route.user_id, metrics=route_metrics
        )

    async def delete_by_id(self, route_id: int) -> None:
        query_result = await self.session.execute(
            select(Route).where(Route.id == route_id, Route.is_deleted == False)
        )
        db_route = query_result.scalar_one_or_none()

        if db_route is None:
            return

        db_route.is_deleted = True
        await self.session.commit()

    async def get_route_by_id(self, route_id: int) -> RouteData | None:
        query_result = await self.session.execute(
            select(Route).where(Route.id == route_id, Route.is_deleted == False)
        )

        db_route = query_result.scalar_one_or_none()

        if db_route is None:
            return None

        geometry_geojson = json.loads(to_geojson(to_shape(db_route.geometry)))

        route_metrics = RouteMetrics(
            distance=db_route.distance_m,
            duration=db_route.duration_s,
            geometry=geometry_geojson,
        )

        return RouteData(
            id=db_route.id,
            user_id=db_route.user_id,
            metrics=route_metrics,
        )

    async def get_routes_by_user_id(self, user_id: int, offset: int, limit: int) -> tuple[list[RouteData], int]:
        query_result = await self.session.execute(
            select(func.count()).where(Route.user_id == user_id, Route.is_deleted == False)
        )

        if query_result is None:
            return [], 0
        
        total = query_result.scalar()

        query_result = await self.session.execute(
            select(Route.id, Route.distance_m, Route.duration_s, Route.user_id, Route.is_deleted)
            .where(Route.user_id == user_id, Route.is_deleted == False)
            .offset(offset)
            .limit(limit)
        )

        user_routes = query_result.all()

        routes: list[RouteData] = []

        for db_route in user_routes:
            geometry_geojson = []
            route_metrics = RouteMetrics(
                distance=db_route.distance_m,
                duration=db_route.duration_s,
                geometry=geometry_geojson,
            )

            routes.append(
                RouteData(
                    id=db_route.id,
                    user_id=db_route.user_id,
                    metrics=route_metrics,
                )
            )

        return routes, total

    async def delete_by_id(self, route_id: int) -> None:
        query_result = await self.session.execute(
            select(Route).where(Route.id == route_id)
        )
        db_route = query_result.scalar_one_or_none()

        if db_route is None:
            return

        db_route.is_deleted = True
        await self.session.commit()
