from typing import Any, Literal

from pydantic import BaseModel, Field

from app.api.schemas.routes.coordinate import CoordinateDTO


class GetRouteMetricsRequest(BaseModel):
    profile: Literal["driving", "walking", "cycling"] = "driving"
    coords: list[CoordinateDTO] = Field(min_length=2)


class GetRouteMetricsResponse(BaseModel):
    distance: float = Field(gt=0)
    duration: float = Field(gt=0)
    geometry: Any
