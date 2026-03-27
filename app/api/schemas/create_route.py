from pydantic import BaseModel, Field
from typing import Any, Literal


class CreateRouteRequest(BaseModel):
    user_id: int = Field(gt=0)
    profile: Literal["driving", "walking", "cycling"] = "driving"
    dots: list[tuple[float, float]]


class CreateRouteResponse(BaseModel):
    route_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    distance: float = Field(gt=0)
    duration: float = Field(gt=0)
    geometry: Any
