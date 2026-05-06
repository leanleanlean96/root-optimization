from pydantic import BaseModel, Field
from typing import Any, Literal


class GetRouteResponse(BaseModel):
    route_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    distance: float = Field(gt=0)
    duration: float = Field(gt=0)
    geometry: Any
