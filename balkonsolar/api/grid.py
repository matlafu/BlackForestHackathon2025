""" Grid demand API client for StromGedacht and OpenGridMap. """
import requests
import logging

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
        self.forecast_url = "https://api.stromgedacht.de/v1/states"
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
            return response["state"]
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
            response_state = response["state"]
            logger.info(f"StromGedacht mapping for zip code: {self.zip_code} is {mappings[response_state]}")
            return mappings[response_state]
        except Exception as e:
            logger.error(f"Error getting StromGedacht mapping for zip code: {self.zip_code}. Error: {e}")
            return "Ungültige Postleitzahl"
        
    async def get_forecast(self) -> list[dict]:
        """
        Get the forecast from the StromGedacht API.
        : return: The forecast from the StromGedacht API as a list of dictionaries
        """
        # Calculate date range for the API request
        from datetime import datetime, timedelta
        
        now = datetime.now()
        from_date = now.strftime("%Y-%m-%dT%H:%M:%S")
        to_date = (now + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")
        
        params = {
            "zip": self.zip_code,
            "from": from_date,
            "to": to_date
        }
        
        logger.info(f"Requesting forecast with params: {params}")
        response = requests.get(self.forecast_url, params=params)
        
        # Check for errors
        if response.status_code != 200:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return response.json()  # Return error for debugging
            
        # The API returns a JSON object, not a list, so we need to extract the forecast
        data = response.json()
        logger.info(f"Received forecast data: {data}")
        
        if isinstance(data, list):
            return data
        elif 'states' in data:
            return data['states'] 
        return data  # Return the full response if we can't determine the format

