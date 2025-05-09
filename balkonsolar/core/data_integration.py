"""
Data integration service for BalkonSolar.
"""
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from loguru import logger

from balkonsolar.api.weather import OpenWeatherMapClient
from balkonsolar.api.electricity import ENTSOEClient
from balkonsolar.api.grid import OpenGridMapClient


class DataIntegrationService:
    """Service for integrating data from various sources."""

    def __init__(
        self,
        weather_api_key: Optional[str] = None,
        entsoe_api_key: Optional[str] = None,
        opengridmap_api_key: Optional[str] = None,
        country_code: str = "DE",
        lat: float = 52.520008,
        lon: float = 13.404954,
    ):
        """
        Initialize the data integration service.

        Args:
            weather_api_key: OpenWeatherMap API key
            entsoe_api_key: ENTSOE API key
            opengridmap_api_key: OpenGridMap API key
            country_code: Country code (e.g., 'DE' for Germany)
            lat: Latitude
            lon: Longitude
        """
        self.weather_client = OpenWeatherMapClient(api_key=weather_api_key)
        self.entsoe_client = ENTSOEClient(api_key=entsoe_api_key)
        self.opengridmap_client = OpenGridMapClient(api_key=opengridmap_api_key)

        self.country_code = country_code
        self.lat = lat
        self.lon = lon

    async def get_weather_data(self) -> Dict[str, Any]:
        """
        Get weather data.

        Returns:
            Weather data
        """
        try:
            current_weather = await self.weather_client.get_current_weather(
                lat=self.lat, lon=self.lon
            )
            forecast = await self.weather_client.get_forecast(
                lat=self.lat, lon=self.lon
            )
            solar_radiation = await self.weather_client.get_solar_radiation(
                lat=self.lat, lon=self.lon
            )

            return {
                "current": current_weather,
                "forecast": forecast,
                "solar": solar_radiation,
            }
        except Exception as e:
            logger.error(f"Error getting weather data: {e}")
            return {}

    async def get_electricity_data(self) -> Dict[str, Any]:
        """
        Get electricity data.

        Returns:
            Electricity data
        """
        try:
            day_ahead_prices = await self.entsoe_client.get_day_ahead_prices(
                country_code=self.country_code
            )
            actual_load = await self.entsoe_client.get_actual_total_load(
                country_code=self.country_code
            )
            forecasted_load = await self.entsoe_client.get_forecasted_total_load(
                country_code=self.country_code
            )

            return {
                "prices": day_ahead_prices,
                "actual_load": actual_load,
                "forecasted_load": forecasted_load,
            }
        except Exception as e:
            logger.error(f"Error getting electricity data: {e}")
            return {}

    async def get_grid_data(self) -> Dict[str, Any]:
        """
        Get grid data.

        Returns:
            Grid data
        """
        try:
            topology = await self.opengridmap_client.get_grid_topology(
                lat=self.lat, lon=self.lon
            )
            load = await self.opengridmap_client.get_grid_load(
                lat=self.lat, lon=self.lon
            )
            stability = await self.opengridmap_client.get_grid_stability(
                lat=self.lat, lon=self.lon
            )
            forecast = await self.opengridmap_client.get_grid_forecast(
                lat=self.lat, lon=self.lon
            )

            return {
                "topology": topology,
                "load": load,
                "stability": stability,
                "forecast": forecast,
            }
        except Exception as e:
            logger.error(f"Error getting grid data: {e}")
            return {}

    async def get_all_data(self) -> Dict[str, Any]:
        """
        Get all data from all sources.

        Returns:
            All data
        """
        weather_data = await self.get_weather_data()
        electricity_data = await self.get_electricity_data()
        grid_data = await self.get_grid_data()

        return {
            "weather": weather_data,
            "electricity": electricity_data,
            "grid": grid_data,
            "timestamp": datetime.now().isoformat(),
        }

    async def get_optimization_data(self) -> Dict[str, Any]:
        """
        Get data needed for optimization.

        Returns:
            Optimization data
        """
        try:
            # Get current weather
            current_weather = await self.weather_client.get_current_weather(
                lat=self.lat, lon=self.lon
            )

            # Get solar forecast for next 24 hours
            now = datetime.now()
            tomorrow = now + timedelta(days=1)
            solar_forecast = await self.weather_client.get_solar_radiation(
                lat=self.lat, lon=self.lon, dt=now
            )

            # Get electricity prices for next 24 hours
            day_ahead_prices = await self.entsoe_client.get_day_ahead_prices(
                country_code=self.country_code,
                start_date=now,
                end_date=tomorrow,
            )

            # Get grid load forecast
            grid_forecast = await self.opengridmap_client.get_grid_forecast(
                lat=self.lat, lon=self.lon,
                start_date=now,
                end_date=tomorrow,
            )

            return {
                "current_weather": current_weather,
                "solar_forecast": solar_forecast,
                "electricity_prices": day_ahead_prices,
                "grid_forecast": grid_forecast,
                "timestamp": now.isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting optimization data: {e}")
            return {}
