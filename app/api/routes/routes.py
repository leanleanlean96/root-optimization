from fastapi import APIRouter, Depends, Path
from app.api.schemas.create_route import CreateRouteRequest, CreateRouteResponse
from app.api.schemas.get_route import GetRouteResponse
from app.api.schemas.get_route_metrics import GetRouteMetricsRequest, GetRouteMetricsResponse
from app.core.dependencies import get_create_route_usecase, get_route_by_id_usecase, get_route_metrics_usecase
from app.application.use_cases.create_route import CreateRouteUseCase
from app.application.use_cases.get_route import GetRouteByIdUseCase
from app.application.use_cases.get_route_metrics import GetRouteMetricsUseCase
from app.application.use_cases.models.create_route import CreateRouteInput, CreateRouteOutput
from app.application.use_cases.models.get_route import GetRouteInput, GetRouteOutput
from app.application.use_cases.models.get_route_metrics import GetRouteMetricsInput, GetRouteMetricsOutput

router = APIRouter(prefix="/routes", tags=["routes"])

@router.post("/create", response_model=CreateRouteResponse, status_code=201)
async def create_route(
    body: CreateRouteRequest,
    usecase: CreateRouteUseCase = Depends(get_create_route_usecase),
):
    result: CreateRouteOutput = await usecase.execute(
        CreateRouteInput(
            user_id=body.user_id,
            coords=body.dots,
            profile=body.profile,
        )
    )

    response: CreateRouteResponse = CreateRouteResponse(
        route_id=result.route_id,
        user_id=result.user_id,
        distance=result.distance,
        duration=result.duration,
        geometry=result.geometry
    )
    #TODO: add status codes
    return response

@router.get("/{route_id}", response_model=GetRouteResponse, status_code=201)
async def create_route(
    route_id: int = Path(gt=0),
    usecase: GetRouteByIdUseCase = Depends(get_route_by_id_usecase),
):
    result: GetRouteOutput = await usecase.execute(
        GetRouteInput(route_id=route_id)
    )

    response: GetRouteResponse = GetRouteResponse(
        route_id=result.route_id,
        user_id=result.user_id,
        distance=result.distance,
        duration=result.duration,
        geometry=result.geometry
    )

    #TODO: add status codes
    return response

@router.post("/metrics", response_model=GetRouteMetricsResponse, status_code=201)
async def create_route(
    body: GetRouteMetricsRequest,
    usecase: GetRouteMetricsUseCase = Depends(get_route_metrics_usecase),
):
    result: GetRouteMetricsOutput = await usecase.execute(
        GetRouteMetricsInput(
            coords=body.dots,
            profile=body.profile,
        )
    )

    response: GetRouteMetricsResponse = GetRouteMetricsResponse(
        distance=result.distance,
        duration=result.duration,
        geometry=result.geometry
    )

    #TODO: add status codes
    return response