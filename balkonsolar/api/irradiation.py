"""
Solar forecast API client for forecast.solar
"""


import requests
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ForecastSolarClient():
    """Client for Forecast.Solar API."""

    def __init__(
            self,
            latitude: float,
            longitude: float,
            declination: float = 0,
            azimuth: float = 180,
            kwp: float = 1.0,
            api_key: Optional[str] = None
    ):
        """
        Initialize the Forecast.Solar API client.

        Args:
            latitude: The latitude of the solar installation
            longitude: The longitude of the solar installation
            declination: The declination/tilt of the panels in degrees (0=horizontal)
            azimuth: The azimuth angle of the panels (180=south)
            kwp: The peak power of the installation in kWp
            api_key: Optional API key for premium features
        """
        self.base_url = "https://api.forecast.solar/"
        self.latitude = latitude
        self.longitude = longitude
        self.declination = declination
        self.azimuth = azimuth
        self.kwp = kwp
        self.api_key = api_key

    async def get_forecast(self) -> dict:
        '''
        Get the response from the Forecast.Solar API.
        Returns: The response from the Forecast.Solar API as a dictionary
        '''
        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "dec": self.declination,
            "az": self.azimuth,
            "kwp": self.kwp
        }

        headers = {}
        if self.api_key:
            headers['X-FORECAST-API-KEY'] = self.api_key

        try:
            params_url_suffix = "estimate/{}/{}/{}/{}/{}".format(
                self.latitude, self.longitude, self.declination, self.azimuth, self.kwp)
            response = requests.get(self.base_url + params_url_suffix, params=params, headers=headers)
            response.raise_for_status()
            return response.json()['result']
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting forecast data: {e}")
            return {}

    async def get_current_power(self) -> float:
        '''
        Get the current estimated power output.
        Returns: Current power output in watts
        '''
        logger.info(f"Getting current power for installation at lat:{self.latitude}, lon:{self.longitude}")
        try:
            response = await self.get_forecast()
            if "result" in response and "watts" in response["result"]:
                watts = response["result"]["watts"]
                if watts:
                    # Get the first (current) value
                    current_time = list(watts.keys())[0]
                    return float(watts[current_time])
            return 0.0
        except Exception as e:
            logger.error(f"Error getting current power: {e}")
            return 0.0

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
    print(forecast.keys())
    watt_forecast = forecast['watts']
    format = "%Y-%m-%dT%H:%M:%S"
    watts = [(datetime.strptime(timestamp, format), watts) for (timestamp, watts) in watt_forecast.items()]
    print(watts[:10])