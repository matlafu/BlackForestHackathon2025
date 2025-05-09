"""
Grid demand API client for OpenGridMap.
"""
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from loguru import logger

from balkonsolar.api.base import BaseAPIClient


class OpenGridMapClient(BaseAPIClient):
    """Client for OpenGridMap API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        cache_ttl: int = 300,  # 5 minutes
    ):
        """
        Initialize the OpenGridMap API client.

        Args:
            api_key: OpenGridMap API key
            timeout: Request timeout in seconds
            cache_ttl: Cache TTL in seconds
        """
        super().__init__(
            base_url="https://api.opengridmap.com/v1",
            api_key=api_key,
            timeout=timeout,
            cache_ttl=cache_ttl,
        )

    async def get_grid_topology(
        self,
        lat: float,
        lon: float,
        radius: float = 10.0,
    ) -> Dict[str, Any]:
        """
        Get grid topology data.

        Args:
            lat: Latitude
            lon: Longitude
            radius: Search radius in kilometers

        Returns:
            Grid topology data
        """
        params = {
            "lat": lat,
            "lon": lon,
            "radius": radius,
            "api_key": self.api_key,
        }

        return await self._request("GET", "/grid/topology", params=params)

    async def get_grid_load(
        self,
        lat: float,
        lon: float,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
    ) -> Dict[str, Any]:
        """
        Get grid load data.

        Args:
            lat: Latitude
            lon: Longitude
            start_date: Start date (defaults to today)
            end_date: End date (defaults to tomorrow)

        Returns:
            Grid load data
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=1)

        if isinstance(start_date, datetime):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, datetime):
            end_date = end_date.strftime("%Y-%m-%d")

        params = {
            "lat": lat,
            "lon": lon,
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }

        return await self._request("GET", "/grid/load", params=params)

    async def get_grid_stability(
        self,
        lat: float,
        lon: float,
    ) -> Dict[str, Any]:
        """
        Get grid stability data.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Grid stability data
        """
        params = {
            "lat": lat,
            "lon": lon,
            "api_key": self.api_key,
        }

        return await self._request("GET", "/grid/stability", params=params)

    async def get_grid_forecast(
        self,
        lat: float,
        lon: float,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
    ) -> Dict[str, Any]:
        """
        Get grid forecast data.

        Args:
            lat: Latitude
            lon: Longitude
            start_date: Start date (defaults to today)
            end_date: End date (defaults to tomorrow)

        Returns:
            Grid forecast data
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=1)

        if isinstance(start_date, datetime):
            start_date = start_date.strftime("%Y-%m-%d")
        if isinstance(end_date, datetime):
            end_date = end_date.strftime("%Y-%m-%d")

        params = {
            "lat": lat,
            "lon": lon,
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }

        return await self._request("GET", "/grid/forecast", params=params)
