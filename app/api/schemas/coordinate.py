from pydantic import BaseModel, Field

from app.domain.models.coordinate import Coordinate


class CoordinateDTO(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)

    def to_domain(self) -> Coordinate:
        return Coordinate(lat=self.lat, lon=self.lon)

    @classmethod
    def from_domain(cls, coord: Coordinate) -> "CoordinateDTO":
        return cls(lat=coord.lat, lon=coord.lon)