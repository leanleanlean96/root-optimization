import httpx
from typing import Tuple

from app.domain.models.route import RouteMetrics


class OsrmClient:
    def __init__(self, service_url: str, client: httpx.AsyncClient):
        self.service_url = service_url
        self.client = client

    async def get_route_metrics(
        self, 
        dots: list[Tuple[float, float]],
        profile: str = "driving"
    ) -> RouteMetrics:
        coords = ";".join(f"{lon},{lat}" for lon, lat in dots)
        url = f"{self.service_url}/route/v1/{profile}/{coords}?geometries=geojson&overview=full"
        
        resp = await self.client.get(url, timeout=30.0)
        resp.raise_for_status()
        
        data = resp.json()
        if data.get("code") != "Ok":
            raise ValueError(f"OSRM error: {data.get('message', 'Unknown')}")
        
        route = data["routes"][0]
        return RouteMetrics(
            distance=route["distance"],
            duration=route["duration"],
            geometry=route["geometry"]
        )