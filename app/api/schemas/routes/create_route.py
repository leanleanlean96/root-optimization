from typing import Any, Literal

from pydantic import BaseModel, Field

from app.api.schemas.routes.coordinate import CoordinateDTO


class CreateRouteRequest(BaseModel):
    user_id: int = Field(gt=0)
    profile: Literal["driving", "walking", "cycling"] = "driving"
    coords: list[CoordinateDTO] = Field(min_length=2)


class CreateRouteResponse(BaseModel):
    route_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    distance: float = Field(gt=0)
    duration: float = Field(gt=0)
    geometry: Any
