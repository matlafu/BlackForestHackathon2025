"""
Base API client with common functionality for all API clients.
"""
import os
import time
from typing import Any, Dict, Optional, Union

import httpx
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv(dotenv_path="balkonsolar/.env")

class BaseAPIClient:
    """Base class for all API clients with common functionality."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        cache_ttl: int = 300,
    ):
        """
        Initialize the base API client.

        Args:
            base_url: The base URL for the API
            api_key: API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            cache_ttl: Cache TTL in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv(f"{self.__class__.__name__.upper()}_API_KEY")
        self.timeout = timeout
        self.max_retries = max_retries
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

        if not self.api_key:
            logger.warning(f"No API key provided for {self.__class__.__name__}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            headers: Additional headers
            use_cache: Whether to use caching

        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Check cache for GET requests
        if method.upper() == "GET" and use_cache:
            cache_key = f"{url}:{str(params)}"
            cached_response = self._get_from_cache(cache_key)
            if cached_response:
                logger.debug(f"Cache hit for {url}")
                return cached_response

        # Prepare headers
        request_headers = headers or {}
        if self.api_key:
            request_headers["Authorization"] = f"Bearer {self.api_key}"

        # Make request
        logger.debug(f"Making {method} request to {url}")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=request_headers,
            )

            # Handle response
            response.raise_for_status()
            result = response.json()

            # Cache GET responses
            if method.upper() == "GET" and use_cache:
                self._add_to_cache(f"{url}:{str(params)}", result)

            return result

    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a value from the cache if it exists and is not expired."""
        if key in self._cache:
            cache_entry = self._cache[key]
            if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                return cache_entry["data"]
            else:
                del self._cache[key]
        return None

    def _add_to_cache(self, key: str, data: Dict[str, Any]) -> None:
        """Add a value to the cache with timestamp."""
        self._cache[key] = {
            "data": data,
            "timestamp": time.time(),
        }

    def clear_cache(self) -> None:
        """Clear the entire cache."""
        self._cache = {}
