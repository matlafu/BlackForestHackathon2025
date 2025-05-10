# test.py
# test the forecast function of StromGedachtClient

import asyncio
import logging

from datetime import datetime, timedelta

from typing import List, Tuple, Optional

from pprint import pprint

from balkonsolar.api.grid import StromGedachtClient

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def forecast_to_array(
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

    start = datetime.fromisoformat(forecast[0]["from"])
    end = datetime.fromisoformat(forecast[-1]["to"])
    result = []

    current = start
    while current < end:
        matched = next(
            (
                entry
                for entry in forecast
                if datetime.fromisoformat(entry["from"])
                <= current
                < datetime.fromisoformat(entry["to"])
            ),
            None,
        )
        timestamp = current.isoformat() if as_str else current
        result.append((timestamp, matched["state"] if matched else None))
        current += timedelta(minutes=resolution_minutes)

    return result


async def main():
    client = StromGedachtClient(zip_code=70173)
    try:
        forecast = await client.get_forecast()

        state_array = forecast_to_array(forecast)
        print("Hourly state array:")
        print(state_array)

        # Handle different potential response formats
        print_more_info = False

        # Add debug output
        print(f"Forecast type: {type(forecast)}")

        # Pretty print for better readability
        print("Forecast content:")
        pprint(forecast)
        if print_more_info:
            if isinstance(forecast, list):
                print("\nParsed forecast data:")
                for hour in forecast:
                    if isinstance(hour, dict):
                        # Adapt based on actual response structure
                        if all(k in hour for k in ["from", "state"]):
                            # Format for cleaner output
                            from_time = (
                                hour["from"].split("T")[1][:5]
                                if "T" in hour["from"]
                                else hour["from"]
                            )
                            print(f"{from_time} → {hour['state']}")
                        else:
                            # Print keys available to help diagnose
                            print(
                                f"Missing expected keys. Available keys: {list(hour.keys())}"
                            )
                            print(f"Entry: {hour}")
                    else:
                        print(f"Unexpected hour format: {hour}")
            elif isinstance(forecast, dict) and "errors" in forecast:
                print("\nAPI returned an error:")
                for error_key, error_msgs in forecast["errors"].items():
                    print(f"  - {error_key}: {', '.join(error_msgs)}")
            else:
                print("Unexpected forecast format - not a list")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
