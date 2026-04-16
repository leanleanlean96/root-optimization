from pydantic import BaseModel, Field
from typing import Any, Literal

from app.api.schemas.coordinate import CoordinateDTO


class CreateRouteRequest(BaseModel):
    user_id: int = Field(gt=0)
    profile: Literal["driving", "walking", "cycling"] = "driving"
    dots: list[CoordinateDTO] = Field(min_length=2)


class CreateRouteResponse(BaseModel):
    route_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    distance: float = Field(gt=0)
    duration: float = Field(gt=0)
    geometry: Any