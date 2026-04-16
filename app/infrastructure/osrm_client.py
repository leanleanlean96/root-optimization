import httpx

from app.domain.models.coordinate import Coordinate
from app.domain.models.route import RouteMetrics
from app.infrastructure.exceptions import (
    OsrmServiceException,
    OsrmServiceUnavailableException,
)


class OsrmClient:
    def __init__(self, service_url: str, client: httpx.AsyncClient):
        self.service_url = service_url
        self.client = client

    async def get_route_metrics(
        self, dots: list[Coordinate], profile: str = "driving"
    ) -> RouteMetrics:
        coords = ";".join(f"{c.lon},{c.lat}" for c in dots)
        url = f"{self.service_url}/route/v1/{profile}/{coords}"
        params = {
            "geometries": "geojson",
            "overview": "full",
        }
        try:
            resp = await self.client.get(url, params=params, timeout=30.0)
            resp.raise_for_status()
        except httpx.TimeoutException:
            raise OsrmServiceUnavailableException("OSRM service timed out")
        except httpx.ConnectError:
            raise OsrmServiceUnavailableException("OSRM service is unavailable")

        data = resp.json()
        if data.get("code") != "Ok":
            raise OsrmServiceException(f"OSRM error: {data.get('message', 'Unknown')}")

        route = data["routes"][0]
        return RouteMetrics(
            distance=route["distance"],
            duration=route["duration"],
            geometry=route["geometry"],
        )

    async def optimize_route(
        self, dots: list[Coordinate], profile: str = "driving"
    ) -> RouteMetrics:
        coords = ";".join(f"{c.lon},{c.lat}" for c in dots)
        url = f"{self.service_url}/trip/v1/{profile}/{coords}"
        params = {
            "roundtrip": "true",
            "source": "first",
            "destination": "any",
            "steps": "false",
            "geometries": "geojson",
            "overview": "full",
        }
        try:
            resp = await self.client.get(url, params=params, timeout=30.0)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise OsrmServiceException(
                f"OSRM returned {e.response.status_code}: {e.response.text}"
            ) from e
        except (
            httpx.TimeoutException,
            httpx.RemoteProtocolError,
            httpx.ConnectError,
        ) as e:
            raise OsrmServiceUnavailableException(f"OSRM unavailable: {e}") from e

        data = resp.json()
        if data.get("code") != "Ok":
            raise OsrmServiceException(f"OSRM error: {data.get('message', 'Unknown')}")

        trip = data["trips"][0]
        return RouteMetrics(
            distance=trip["distance"],
            duration=trip["duration"],
            geometry=trip["geometry"],
        )
