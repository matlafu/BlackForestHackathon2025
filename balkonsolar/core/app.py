"""
Balkonsolar System Advisor CLI

This script pulls together rules, battery data, and grid demand to provide a system status and recommendation for the Balkonsolar setup. Intended for command-line use or integration/testing.
"""
# basically pull all the rules and battery data from rules.py and battery.py

import rootutils

root = rootutils.setup_root(__file__, pythonpath=True)

from balkonsolar.core.rules import determine_balkonsolar_state
from balkonsolar.core.database_interface import DatabaseInterface
from balkonsolar.api.grid import StromGedachtClient

def run_balkonsolar_advisor():
    """
    Run the Balkonsolar system advisor.
    Fetches current battery, solar, and grid data, then determines and prints the optimal system state.
    """
    # Get user inputs with reasonable defaults
    print("===== Balkonsolar System Advisor =====")

    # These are user data, which we will get in input "usually"
    # but currently they are "hardcoded".
    zip_code = "10115"
    max_solar_capacity = 400
    # the following are user inputs, right now BatteryController assumes a
    # max_battery_capacity of 2.560
    max_battery_capacity = 2.560
    min_battery_percent = 0.25


    # Get grid demand from API based on zip code
    stromGedachtClient = StromGedachtClient(zip_code=zip_code)

    # Use DatabaseInterface to access energy data
    db = DatabaseInterface()

    try:
        # Get data from the database
        battery_status = db.get_battery_status()
        current_solar_production = db.get_solar_output()
        if current_solar_production == 0:
            # Use a default value for demo if no data in database
            current_solar_production = 250

        current_battery_percent = battery_status.get("percent_full", 0)

        # Get grid demand from API based on zip code
        print(f"\nFetching grid demand data for ZIP code {zip_code}...")
        current_grid_demand = stromGedachtClient.get_stromgedacht_mapping_integer()

        # Determine optimal system state
        state = determine_balkonsolar_state(
            current_grid_demand,
            current_solar_production,
            current_battery_percent,
            max_solar_capacity,
            min_battery_percent,
        )

        # Display system status and recommendation
        print("\n===== System Status =====")
        print(f"Solar Production: {current_solar_production}W / {max_solar_capacity}W")
        print(f"Battery Charge: {battery_status.get('current_charge_kwh', 0):.2f} / {max_battery_capacity}kWh " +
              f"({current_battery_percent:.1f}%)")

        print("\n===== Recommendation =====")
        print(f"Optimal state: {state}")


    except ValueError as e:
        print(f"Error processing input: {e}")
        print("Please enter valid numeric values.")



# If this file is run directly, start the advisor
if __name__ == "__main__":
    run_balkonsolar_advisor()
