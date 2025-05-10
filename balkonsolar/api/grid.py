"""
Grid demand API client for StromGedacht and OpenGridMap.
"""
import requests
from typing import Optional
import logging
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StromGedachtClient():
    """Client for StromGedacht API."""

    def __init__(
        self,
        zip_code: int|None = None
    ):
        """
        Initialize the StromGedacht API client.

        Args:
            zip_code: The zip code of the location to get the grid load for
        """
        self.base_url = "https://api.stromgedacht.de/v1/now"
        self.zip_code = zip_code
    
    @staticmethod
    async def get_stromgedacht_mapping():
        return {
            -1 : 'Ideally use electricity now',
            1 : 'Normal operation',
            3 : 'Reduce consumption (save cost & CO2)',
            4 : 'Reduce consumption (prevent power shortfalls)'
        }
    
    @staticmethod
    async def get_stromgedacht_mapping_german():
        return {
            -1 : 'Strom jetzt nutzen, um die Netzdienlichkeit zu unterstützen',
            1 : 'Normalbetrieb – Du musst nichts weiter tun',
            3 : 'Verbrauch reduzieren, um Kosten und CO2 zu sparen',
            4 : 'Verbrauch reduzieren, um Strommangel zu verhindern'
        }

    async def get_stromgedacht_api_response(self) -> dict:
        '''
        Get the response from the StromGedacht API.
        : return: The response from the StromGedacht API as a dictionary
        '''
        params = {
            "zip": self.zip_code
        }
        response = requests.get(self.base_url, params=params)
        return response.json()
    
    async def get_stromgedacht_mapping_integer(
        self,
    ) -> int|None:
        '''
        Get the mapping of the StromGedacht API.
        : return: The mapping of the StromGedacht API as an integer
        '''
        logger.info(f"Getting StromGedacht integer mapping for zip code: {self.zip_code}")
        response = await self.get_stromgedacht_api_response()
        try:
            return response.json()["state"]
        except Exception as e:
            logger.error(f"Error getting StromGedacht integer mapping for zip code: {self.zip_code}. Error: {e}")
            return None

    async def get_stromgedacht_mapping_state(
        self,
    ) -> str:
        """
        Get the mapping of the Strom Gedacht API.
        : return: The mapping of the Strom Gedacht API as a string
        """
        logger.info(f"Getting StromGedacht mapping for zip code: {self.zip_code}")
        response = await self.get_stromgedacht_api_response()
        mappings = await self.get_stromgedacht_mapping_german()
        try:
            response_state = response.json()["state"]
            logger.info(f"StromGedacht mapping for zip code: {self.zip_code} is {mappings[response_state]}")
            return mappings[response_state]
        except Exception as e:
            logger.error(f"Error getting StromGedacht mapping for zip code: {self.zip_code}. Error: {e}")
            return "Ungültige Postleitzahl"
    

