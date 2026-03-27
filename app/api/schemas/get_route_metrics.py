from pydantic import BaseModel, Field
from typing import Any, Literal

class GetRouteMetricsRequest(BaseModel):
    profile: Literal["driving", "walking", "cycling"] = "driving"
    dots: list[tuple[float, float]]

class GetRouteMetricsResponse(BaseModel):
    distance: float = Field(gt=0)
    duration: float = Field(gt=0)
    geometry: Any