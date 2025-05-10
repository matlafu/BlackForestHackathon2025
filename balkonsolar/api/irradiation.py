"""
Solar forecast API client for forecast.solar
"""

import time
from typing import Optional
import requests
import logging
import os
from datetime import datetime, timedelta
from diskcache import Cache
from core.database_interface import DatabaseInterface

logger = logging.getLogger(__name__)

class ForecastSolarClient():
    """Client for Forecast.Solar API with persistent caching."""

    def __init__(
            self,
            latitude: float,
            longitude: float,
            declination: float = 0,
            azimuth: float = 180,
            kwp: float = 1.0,
            api_key: Optional[str] = None,
            cache_dir: str = ".forecast_solar_cache",
            cache_ttl: int = 3600  # 1 hour default TTL in seconds
    ):
        """
        Initialize the Forecast.Solar API client with caching.

        Args:
            latitude: The latitude of the solar installation
            longitude: The longitude of the solar installation
            declination: The declination/tilt of the panels in degrees (0=horizontal)
            azimuth: The azimuth angle of the panels (180=south)
            kwp: The peak power of the installation in kWp
            api_key: Optional API key for premium features
            cache_dir: Directory for cache storage
            cache_ttl: Time-to-live for cache entries in seconds
        """
        self.base_url = "https://api.forecast.solar/"
        self.latitude = latitude
        self.longitude = longitude
        self.declination = declination
        self.azimuth = azimuth
        self.kwp = kwp
        self.api_key = api_key
        self.cache_ttl = cache_ttl
        
        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize disk cache
        self.cache = Cache(cache_dir)

    def _get_cache_key(self) -> str:
        """Generate a unique cache key based on installation parameters."""
        return f"forecast_{self.latitude}_{self.longitude}_{self.declination}_{self.azimuth}_{self.kwp}"

    async def get_forecast(self) -> dict:
        '''
        Get the response from the Forecast.Solar API with caching.
        Returns: The response from the Forecast.Solar API as a dictionary
        '''
        cache_key = self._get_cache_key()
        
        # Try to get from cache first
        cached_data = self.cache.get(cache_key)
        if cached_data is not None:
            timestamp, data = cached_data
            # Check if the cached data is still valid based on TTL
            if time.time() - timestamp <= self.cache_ttl:
                logger.info("Using cached forecast data")
                return data
        
        headers = {}
        if self.api_key:
            headers['X-FORECAST-API-KEY'] = self.api_key

        try:
            params_url_suffix = f"estimate/{self.latitude}/{self.longitude}/{self.declination}/{self.azimuth}/{self.kwp}"
            response = requests.get(self.base_url + params_url_suffix, headers=headers)
            response.raise_for_status()
            result = response.json().get('result', {})
            
            # Store in cache with current timestamp
            self.cache[cache_key] = (time.time(), result)
            
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting forecast data: {e}")
            return {}

    async def get_watt_hours(self) -> dict:
        forecast = await  client.get_forecast()
        watt_hour_forecast = forecast["watt_hours"]
        format = "%Y-%m-%d %H:%M:%S"
        return { datetime.strptime(timestamp, format): watts for (timestamp, watts) in
                      watt_hour_forecast.items() }

    async def get_current_power(self) -> float:
        '''
        Get the current estimated power output.
        Returns: Current power output in watts
        '''
        logger.info(f"Getting current power for installation at lat:{self.latitude}, lon:{self.longitude}")
        try:
            response = await self.get_forecast()
            if "watts" in response:
                watts = response["watts"]
                if watts:
                    # Get the first (current) value
                    current_time = list(watts.keys())[0]
                    return float(watts[current_time])
            return 0.0
        except Exception as e:
            logger.error(f"Error getting current power: {e}")
            return 0.0
            
    def clear_cache(self):
        """Clear all cache entries."""
        self.cache.clear()
        
    def set_cache_ttl(self, ttl_seconds: int):
        """Update the TTL for cache entries.
        
        Args:
            ttl_seconds: New TTL value in seconds
        """
        self.cache_ttl = ttl_seconds
    
    def save_irradiation_data_to_database(self, value: float, timestamp: Optional[str] = None):
        '''
        Save the irradiation data to the database.
        '''
        # TODO: FINISH THIS
        db = DatabaseInterface()
        db.store_irradiation_data(value, timestamp)

if __name__ == "__main__":
    if __name__ == '__main__':
        import asyncio

        client = ForecastSolarClient(
            latitude=52.520008,
            longitude=13.404954,
            declination=30,
            azimuth=0,
            kwp=0.8,
        )
        forecast = asyncio.run(client.get_forecast())
        watt_forecast = forecast["watts"]
        watt_hour_forecast = forecast["watt_hours"]
        format = "%Y-%m-%d %H:%M:%S"
        watt_hours = asyncio.run(client.get_watt_hours())
        print(list(watt_hours.items())[:10])

        import pandas as pd

        print(pd.DataFrame(list(watt_hours.items())).set_index(0).head())
