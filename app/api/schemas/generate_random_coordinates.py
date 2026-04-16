from pydantic import BaseModel, Field

from app.api.schemas.coordinate import CoordinateDTO


class GenerateRandomCoordinatesRequest(BaseModel):
    count: int = Field(ge=2, le=100)


class GenerateRandomCoordinatesResponse(BaseModel):
    coords: list[CoordinateDTO]