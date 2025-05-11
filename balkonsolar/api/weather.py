"""
Weather API client for OpenWeatherMap.
"""
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="balkonsolar/.env")
from datetime import datetime
from typing import Dict, List, Optional, Union

from loguru import logger

from balkonsolar.api.base import BaseAPIClient


class OpenWeatherMapClient(BaseAPIClient):
    """Client for OpenWeatherMap API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        cache_ttl: int = 900,  # 15 minutes
    ):
        """
        Initialize the OpenWeatherMap API client.

        Args:
            api_key: OpenWeatherMap API key
            timeout: Request timeout in seconds
            cache_ttl: Cache TTL in seconds
        """
        super().__init__(
            base_url="https://api.openweathermap.org/data/2.5",
            api_key=api_key or os.getenv("OPENWEATHERMAP_API_KEY"),
            timeout=timeout,
            cache_ttl=cache_ttl,
        )

    async def get_current_weather(
        self, lat: float, lon: float, units: str = "metric"
    ) -> Dict[str, Any]:
        """
        Get current weather data.

        Args:
            lat: Latitude
            lon: Longitude
            units: Units (metric, imperial)

        Returns:
            Current weather data
        """
        params = {
            "lat": lat,
            "lon": lon,
            "units": units,
            "appid": self.api_key,
        }

        return await self._request("GET", "/weather", params=params)

    async def get_forecast(
        self, lat: float, lon: float, units: str = "metric"
    ) -> Dict[str, Any]:
        """
        Get 5-day/3-hour forecast.

        Args:
            lat: Latitude
            lon: Longitude
            units: Units (metric, imperial)

        Returns:
            5-day/3-hour forecast data
        """
        params = {
            "lat": lat,
            "lon": lon,
            "units": units,
            "appid": self.api_key,
        }

        return await self._request("GET", "/forecast", params=params)

    async def get_solar_radiation(
        self, lat: float, lon: float, dt: Optional[Union[int, datetime]] = None
    ) -> Dict[str, Any]:
        """
        Get solar radiation data.

        Args:
            lat: Latitude
            lon: Longitude
            dt: Timestamp or datetime (defaults to current time)

        Returns:
            Solar radiation data
        """
        if isinstance(dt, datetime):
            dt = int(dt.timestamp())

        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }

        if dt:
            params["dt"] = dt

        return await self._request("GET", "/solar", params=params)

    async def get_air_pollution(
        self, lat: float, lon: float
    ) -> Dict[str, Any]:
        """
        Get air pollution data.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Air pollution data
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }

        return await self._request("GET", "/air_pollution", params=params)

    async def get_air_pollution_forecast(
        self, lat: float, lon: float
    ) -> Dict[str, Any]:
        """
        Get air pollution forecast.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Air pollution forecast data
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }

        return await self._request("GET", "/air_pollution/forecast", params=params)
