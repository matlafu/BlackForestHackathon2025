"""
Electricity price API client for ENTSOE.
"""
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="balkonsolar/.env")
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from loguru import logger

from balkonsolar.api.base import BaseAPIClient


class ENTSOEClient(BaseAPIClient):
    """Client for ENTSOE API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        cache_ttl: int = 300,  # 5 minutes
    ):
        """
        Initialize the ENTSOE API client.

        Args:
            api_key: ENTSOE API key
            timeout: Request timeout in seconds
            cache_ttl: Cache TTL in seconds
        """
        super().__init__(
            base_url="https://transparency.entsoe.eu/api",
            api_key=api_key or os.getenv("ENTSOE_API_KEY"),
            timeout=timeout,
            cache_ttl=cache_ttl,
        )

    async def get_day_ahead_prices(
        self,
        country_code: str,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
    ) -> Dict[str, Any]:
        """
        Get day-ahead electricity prices.

        Args:
            country_code: Country code (e.g., 'DE' for Germany)
            start_date: Start date (defaults to today)
            end_date: End date (defaults to tomorrow)

        Returns:
            Day-ahead electricity prices
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=1)

        if isinstance(start_date, datetime):
            start_date = start_date.strftime("%Y%m%d")
        if isinstance(end_date, datetime):
            end_date = end_date.strftime("%Y%m%d")

        params = {
            "securityToken": self.api_key,
            "documentType": "A44",
            "in_Domain": self._get_domain(country_code),
            "out_Domain": self._get_domain(country_code),
            "periodStart": start_date,
            "periodEnd": end_date,
        }

        return await self._request("GET", "", params=params)

    async def get_actual_total_load(
        self,
        country_code: str,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
    ) -> Dict[str, Any]:
        """
        Get actual total load.

        Args:
            country_code: Country code (e.g., 'DE' for Germany)
            start_date: Start date (defaults to today)
            end_date: End date (defaults to tomorrow)

        Returns:
            Actual total load data
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=1)

        if isinstance(start_date, datetime):
            start_date = start_date.strftime("%Y%m%d")
        if isinstance(end_date, datetime):
            end_date = end_date.strftime("%Y%m%d")

        params = {
            "securityToken": self.api_key,
            "documentType": "A65",
            "processType": "A16",
            "outBiddingZone_Domain": self._get_domain(country_code),
            "periodStart": start_date,
            "periodEnd": end_date,
        }

        return await self._request("GET", "", params=params)

    async def get_forecasted_total_load(
        self,
        country_code: str,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
    ) -> Dict[str, Any]:
        """
        Get forecasted total load.

        Args:
            country_code: Country code (e.g., 'DE' for Germany)
            start_date: Start date (defaults to today)
            end_date: End date (defaults to tomorrow)

        Returns:
            Forecasted total load data
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=1)

        if isinstance(start_date, datetime):
            start_date = start_date.strftime("%Y%m%d")
        if isinstance(end_date, datetime):
            end_date = end_date.strftime("%Y%m%d")

        params = {
            "securityToken": self.api_key,
            "documentType": "A65",
            "processType": "A01",
            "outBiddingZone_Domain": self._get_domain(country_code),
            "periodStart": start_date,
            "periodEnd": end_date,
        }

        return await self._request("GET", "", params=params)

    def _get_domain(self, country_code: str) -> str:
        """
        Get ENTSOE domain code for a country.

        Args:
            country_code: Country code (e.g., 'DE' for Germany)

        Returns:
            ENTSOE domain code
        """
        domains = {
            "DE": "10Y1001A1001A83F",  # Germany
            "FR": "10Y1001A1001A87F",  # France
            "NL": "10Y1001A1001A93F",  # Netherlands
            "BE": "10Y1001A1001A81F",  # Belgium
            "AT": "10Y1001A1001A83F",  # Austria
            "CH": "10Y1001A1001A83F",  # Switzerland
            "IT": "10Y1001A1001A73F",  # Italy
            "ES": "10Y1001A1001A65F",  # Spain
            "PT": "10Y1001A1001A65F",  # Portugal
            "DK": "10Y1001A1001A65F",  # Denmark
            "SE": "10Y1001A1001A44F",  # Sweden
            "NO": "10Y1001A1001A48F",  # Norway
            "FI": "10Y1001A1001A44F",  # Finland
            "PL": "10Y1001A1001A83F",  # Poland
            "CZ": "10Y1001A1001A83F",  # Czech Republic
            "SK": "10Y1001A1001A83F",  # Slovakia
            "HU": "10Y1001A1001A83F",  # Hungary
            "RO": "10Y1001A1001A83F",  # Romania
            "BG": "10Y1001A1001A83F",  # Bulgaria
            "GR": "10Y1001A1001A83F",  # Greece
            "IE": "10Y1001A1001A83F",  # Ireland
            "GB": "10Y1001A1001A83F",  # Great Britain
        }

        return domains.get(country_code.upper(), "10Y1001A1001A83F")  # Default to Germany
