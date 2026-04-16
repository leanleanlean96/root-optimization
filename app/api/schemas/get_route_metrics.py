from pydantic import BaseModel, Field
from typing import Any, Literal

from app.api.schemas.coordinate import CoordinateDTO


class GetRouteMetricsRequest(BaseModel):
    profile: Literal["driving", "walking", "cycling"] = "driving"
    dots: list[CoordinateDTO] = Field(min_length=2)


class GetRouteMetricsResponse(BaseModel):
    distance: float = Field(gt=0)
    duration: float = Field(gt=0)
    geometry: Any