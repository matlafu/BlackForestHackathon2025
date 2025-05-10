"""
Grid demand API client for StromGedacht and OpenGridMap.
"""
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

import logging

from balkonsolar.api.base import BaseAPIClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StromGedachtClient(BaseAPIClient):
    """Client for StromGedacht API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        cache_ttl: int = 300,  # 5 minutes
        zip_code: int|None = None
    ):
        """
        Initialize the StromGedacht API client.

        Args:
            api_key: StromGedacht API key
            timeout: Request timeout in seconds
            cache_ttl: Cache TTL in seconds
        """
        super().__init__(
            base_url="https://api.stromgedacht.de/v1/now",
            api_key=api_key,
            timeout=timeout,
            cache_ttl=cache_ttl,
            zip_code=zip_code
        )
    
    @staticmethod
    async def get_stromgedacht_mapping():
        return {
            -1 : 'Ideally use electricity now',
            1 : 'Normal operation',
            3 : 'Reduce consumption (save cost & CO2)',
            4 : 'Reduce consumption (prevent power shortfalls)'
        }

    async def get_grid_load(
        self,
        zip_code: Optional[int|None] = None
    ) -> Dict[int, str]:
        """
        Get the mapping of the Strom Gedacht API.
        Mappings:
        -1: Ideally use electricity now
        1: Normal operation
        """
        # Use the base zip code if not provided
        zip_code = self.zip_code if zip_code is None else zip_code
        params = {
            "zip": zip_code
        }
        response = await self._request("GET", self.base_url, params=params)
        mappings = await self.get_stromgedacht_mapping()
        if response.get("status") == "success":
            return mappings[response.get("value")]
        else:
            return {
                "status": "error",
                "message": response.get("message")
            }


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
