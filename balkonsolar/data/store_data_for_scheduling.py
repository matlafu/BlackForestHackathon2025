import asyncio
import itertools
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Iterator

import pandas as pd

from balkonsolar.api.grid import StromGedachtClient
from balkonsolar.api.irradiation import ForecastSolarClient
from balkonsolar.core.database_interface import DatabaseInterface


def store_solar_production_predictions():
    """
    Fetch solar production forecast from the ForecastSolar API and store it in the database.
    """
    (lat, lon) = (48.0173627,7.8272418) # the FRIZ
    client = ForecastSolarClient(
        latitude=lat,
        longitude=lon,
        declination=30,
        azimuth=0,
        kwp=0.8,
    )
    watt_hours_dict = asyncio.run(client.get_watt_hours())
    watt_hours_df = pd.DataFrame(list(watt_hours_dict.items())).rename(columns={0: "timestamp", 1: "watt_hours"})
    watt_hours_df = watt_hours_df.sort_values(by="timestamp")

    dbi = DatabaseInterface()
    dbi.store_irradiation_data(watt_hours_df)

def __grid_forecast_to_array(
    forecast: List[dict], resolution_minutes: int = 60, as_str: bool = False
) -> List[Tuple[datetime | str, Optional[int]]]:
    """
    Converts forecast states into a time series of (timestamp, state) tuples.

    Args:
        forecast: List of forecast intervals with "from", "to", and "state".
        resolution_minutes: How often to sample the forecast (default: 60 mins).
        as_str: If True, timestamps are returned as ISO-formatted strings.

    Returns:
        List of (timestamp, state) tuples.
    """
    if not forecast:
        return []

    def _expand_interval(interval: dict) -> Iterator[Tuple[datetime, int]]:
        start = datetime.fromisoformat(interval["from"])
        end = datetime.fromisoformat(interval["to"])
        state = interval["state"]
        return map(lambda dt: (dt, state), __full_hours_in_interval(start, end))

    return list(itertools.chain.from_iterable(_expand_interval(d) for d in forecast))

def __full_hours_in_interval(
        start_dt: datetime,
        end_dt: datetime
) -> Iterator[datetime]:
    start_hour = start_dt.replace(minute=0, second=0, microsecond=0)
    if start_dt != start_hour:
        start_hour += timedelta(hours=1)

    end_hour = end_dt.replace(minute=0, second=0, microsecond=0)

    hours_iter = itertools.takewhile(
        lambda dt: dt < end_hour,
        (start_hour + timedelta(hours=i) for i in range(1000000))  # Large enough range
    )

    return hours_iter


def store_grid_state_predictions():
    """
    Fetch grid state forecast from the StromGedacht API and store it in the database.
    """
    client = StromGedachtClient(zip_code=79110)
    grid_forecast = asyncio.run(client.get_forecast())

    state_array = __grid_forecast_to_array(grid_forecast)
    grid_state_df = pd.DataFrame(state_array, columns=["timestamp", "grid_state"])
    grid_state_df = grid_state_df.sort_values(by="timestamp")

    dbi = DatabaseInterface()
    dbi.store_grid_usage_forecast(grid_state_df)

def main():
    """
    Fetch and store both solar production and grid state predictions.
    """
    store_solar_production_predictions()
    store_grid_state_predictions()

if __name__ == "__main__":
    main()
