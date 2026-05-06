import math

from fastapi import APIRouter, Depends, Path

from app.api.schemas.routes.coordinate import CoordinateDTO
from app.api.schemas.routes.create_route import CreateRouteRequest, CreateRouteResponse
from app.api.schemas.routes.generate_random_coordinates import (
    GenerateRandomCoordinatesRequest,
    GenerateRandomCoordinatesResponse,
)
from app.api.schemas.routes.get_all_user_routes import PaginatedRoutes, PaginationParams
from app.api.schemas.routes.get_route import GetRouteResponse
from app.api.schemas.routes.get_route_metrics import (
    GetRouteMetricsRequest,
    GetRouteMetricsResponse,
)
from app.application.models.create_route import (
    CreateRouteInput,
    CreateRouteOutput,
)
from app.application.models.generate_random_coordinates import (
    GenerateRandomCoordinatesInput,
)
from app.application.models.get_route import GetRouteInput, GetRouteOutput
from app.application.models.get_route_metrics import (
    GetRouteMetricsInput,
    GetRouteMetricsOutput,
)
from app.application.use_cases.routes.create_route import CreateRouteUseCase
from app.application.use_cases.routes.delete_route import DeleteRouteUseCase
from app.application.use_cases.routes.delete_route import DeleteRouteUseCase
from app.application.use_cases.routes.generate_random_coordinates import (
    GenerateRandomCoordinatesUseCase,
)
from app.application.use_cases.routes.get_route import GetAllUserRoutesUseCase, GetRouteByIdUseCase
from app.application.use_cases.routes.get_route_metrics import GetRouteMetricsUseCase
from app.core.auth.models import UserClaims
from app.core.dependencies import (
    get_create_route_usecase,
    get_delete_route_usecase,
    get_generate_random_coordinates_usecase,
    get_get_all_routes_by_user_id_usecase,
    get_optimize_route_usecase,
    get_route_by_id_usecase,
    get_route_metrics_usecase,
    get_user_claims,
)

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post("/create", response_model=CreateRouteResponse, status_code=201)
async def create_route(
    body: CreateRouteRequest,
    claims: UserClaims = Depends(get_user_claims),
    usecase: CreateRouteUseCase = Depends(get_create_route_usecase),
):
    result: CreateRouteOutput = await usecase.execute(
        CreateRouteInput(
            user_id=claims.user_id,
            coords=[dot.to_domain() for dot in body.coords],
            profile=body.profile,
        )
    )
    return CreateRouteResponse(
        route_id=result.route_id,
        user_id=result.user_id,
        distance=result.distance,
        duration=result.duration,
        geometry=result.geometry,
    )

@router.delete("/{route_id}", status_code=204)
async def delete_route(
    route_id: int = Path(gt=0),
    claims: UserClaims = Depends(get_user_claims),
    usecase: DeleteRouteUseCase = Depends(get_delete_route_usecase),
):
    await usecase.execute(route_id)

@router.get("/{route_id}", response_model=GetRouteResponse, status_code=200)
async def get_route_by_id(
    route_id: int = Path(gt=0),
    claims: UserClaims = Depends(get_user_claims),
    usecase: GetRouteByIdUseCase = Depends(get_route_by_id_usecase),
):
    result: GetRouteOutput = await usecase.execute(GetRouteInput(route_id=route_id))
    return GetRouteResponse(
        route_id=result.route_id,
        user_id=result.user_id,
        distance=result.distance,
        duration=result.duration,
        geometry=result.geometry,
    )

@router.get("/all/me", response_model=PaginatedRoutes)
async def get_all_user_routes(
    claims: UserClaims = Depends(get_user_claims),
    pagination: PaginationParams = Depends(),
    usecase: GetAllUserRoutesUseCase = Depends(get_get_all_routes_by_user_id_usecase),
):
    routes, total = await usecase.execute(
        user_id=claims.user_id,
        offset=pagination.offset,
        limit=pagination.page_size,
    )
    return PaginatedRoutes(
        items=[GetRouteResponse(
            route_id=route.route_id,
            user_id=route.user_id,
            distance=route.distance,
            duration=route.duration,
            geometry=route.geometry,
        ) for route in routes],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=math.ceil(total / pagination.page_size),
    )

@router.post("/metrics", response_model=GetRouteMetricsResponse, status_code=200)
async def get_route_metrics(
    body: GetRouteMetricsRequest,
    usecase: GetRouteMetricsUseCase = Depends(get_route_metrics_usecase),
):
    result: GetRouteMetricsOutput = await usecase.execute(
        GetRouteMetricsInput(
            coords=[dot.to_domain() for dot in body.coords],
            profile=body.profile,
        )
    )
    return GetRouteMetricsResponse(
        distance=result.distance,
        duration=result.duration,
        geometry=result.geometry,
    )


@router.post("/optimize", response_model=GetRouteMetricsResponse, status_code=200)
async def optimize_route(
    body: GetRouteMetricsRequest,
    usecase: GetRouteMetricsUseCase = Depends(get_optimize_route_usecase),
):
    result: GetRouteMetricsOutput = await usecase.execute(
        GetRouteMetricsInput(
            coords=[dot.to_domain() for dot in body.coords],
            profile=body.profile,
        )
    )
    return GetRouteMetricsResponse(
        distance=result.distance,
        duration=result.duration,
        geometry=result.geometry,
    )


@router.post(
    "/random-coordinates",
    response_model=GenerateRandomCoordinatesResponse,
    status_code=200,
)
async def random_coordinates(
    body: GenerateRandomCoordinatesRequest,
    usecase: GenerateRandomCoordinatesUseCase = Depends(
        get_generate_random_coordinates_usecase
    ),
):
    result = await usecase.execute(GenerateRandomCoordinatesInput(count=body.count))
    return GenerateRandomCoordinatesResponse(
        coords=[CoordinateDTO.from_domain(c) for c in result.coords],
    )
