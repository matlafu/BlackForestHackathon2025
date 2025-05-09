"""
Data models for BalkonSolar.
"""
from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    """Weather data model."""
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., description="Humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    wind_direction: float = Field(..., description="Wind direction in degrees")
    cloud_cover: float = Field(..., description="Cloud cover percentage")
    precipitation: float = Field(..., description="Precipitation in mm")
    solar_radiation: float = Field(..., description="Solar radiation in W/m²")
    timestamp: datetime = Field(..., description="Timestamp of the measurement")


class WeatherForecast(BaseModel):
    """Weather forecast data model."""
    forecasts: List[WeatherData] = Field(..., description="List of weather forecasts")
    timestamp: datetime = Field(..., description="Timestamp of the forecast")


class ElectricityPrice(BaseModel):
    """Electricity price data model."""
    price: float = Field(..., description="Price in EUR/MWh")
    timestamp: datetime = Field(..., description="Timestamp of the price")
    market: str = Field(..., description="Market (e.g., 'day-ahead')")
    country_code: str = Field(..., description="Country code")


class GridLoad(BaseModel):
    """Grid load data model."""
    load: float = Field(..., description="Load in MW")
    timestamp: datetime = Field(..., description="Timestamp of the load")
    country_code: str = Field(..., description="Country code")
    is_forecast: bool = Field(..., description="Whether this is a forecast")


class GridStability(BaseModel):
    """Grid stability data model."""
    frequency: float = Field(..., description="Grid frequency in Hz")
    voltage: float = Field(..., description="Grid voltage in V")
    stability_index: float = Field(..., description="Grid stability index")
    timestamp: datetime = Field(..., description="Timestamp of the measurement")
    location: Dict[str, float] = Field(..., description="Location (lat, lon)")


class OptimizationData(BaseModel):
    """Data model for optimization."""
    current_weather: WeatherData = Field(..., description="Current weather data")
    solar_forecast: WeatherForecast = Field(..., description="Solar forecast data")
    electricity_prices: List[ElectricityPrice] = Field(..., description="Electricity prices")
    grid_forecast: List[GridLoad] = Field(..., description="Grid load forecast")
    timestamp: datetime = Field(..., description="Timestamp of the data")


class IntegratedData(BaseModel):
    """Integrated data model."""
    weather: Dict[str, Union[WeatherData, WeatherForecast]] = Field(..., description="Weather data")
    electricity: Dict[str, Union[List[ElectricityPrice], List[GridLoad]]] = Field(..., description="Electricity data")
    grid: Dict[str, Union[GridStability, List[GridLoad]]] = Field(..., description="Grid data")
    timestamp: datetime = Field(..., description="Timestamp of the data")
