from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeleteRouteInput:
    route_id: int
