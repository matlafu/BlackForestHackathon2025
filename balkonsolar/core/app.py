# basically pull all the rules and battery data from rules.py and battery.py

import rootutils

root = rootutils.setup_root(__file__, pythonpath=True)

from balkonsolar.core.rules import determine_balkonsolar_state
from balkonsolar.appdaemon.apps.battery_controller import BatteryController
from balkonsolar.api.grid import StromGedachtClient

def run_balkonsolar_advisor():
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
    
    battery = BatteryController()
    
    try:
        # For demonstration purposes, simulate current values
        # In a real implementation, you would fetch these from sensors or APIs
        current_solar_production = 250
        current_battery_percent = battery.get_battery_status()["percent_full"]
        
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
        print(f"Battery Charge: {current_battery_percent} / {max_battery_capacity}Wh " + 
              f"({int(current_battery_percent/max_battery_capacity*100)}%)")
        
        print("\n===== Recommendation =====")
        print(f"Optimal state: {state}")
        
        
    except ValueError as e:
        print(f"Error processing input: {e}")
        print("Please enter valid numeric values.")
    


# If this file is run directly, start the advisor
if __name__ == "__main__":
    run_balkonsolar_advisor()
