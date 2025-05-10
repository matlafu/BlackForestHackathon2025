"""
Balkonsolar System Optimization Algorithm

This algorithm determines the optimal operating state for a Balkonsolar system
based on current grid demand, solar production, and battery capacity.

States:
0 - Use solar to power household
1 - Charge battery from solar
2 - Use battery to power household
3 - Use grid to power household

Args:
    grid_demand (int): Current grid demand level from Stromgedacht API (0, 1, or 2)
    solar_production (float): Current solar production (Watts)
    current_battery_percent (float): Current battery capacity (percentage)
    max_solar_capacity (float): Maximum solar production capacity (Watts)
    max_battery_percent (float): Maximum battery capacity (percentage)
    min_battery_percent (float): Minimum desired battery charge level (percentage)
    
Returns:
    int: The recommended state (0-3)
"""

USER_SOLAR_HIGH_THRESHOLD = 0.50
STROMGEDACHT_HIGH_THRESHOLD = 1


def determine_balkonsolar_state(
    grid_demand,
    solar_production,
    max_battery_capacity, # get from user
    current_battery_capacity, # we get this from moritz, 
    max_solar_capacity, #user
    battery_high_threshold = 0.8, # we get this from user
    min_battery_percent = 0.25 # we get this from user
):
    # Define thresholds for solar production (high if > 50% of maximum capacity)
    solar_high_threshold = USER_SOLAR_HIGH_THRESHOLD * max_solar_capacity
    current_battery_percent = current_battery_capacity/max_battery_capacity
    # Convert raw values to binary states
    is_grid_demand_high = grid_demand > STROMGEDACHT_HIGH_THRESHOLD  # Stromgedacht API: 0=low, 1 or 2=high
    is_solar_production_high = solar_production > solar_high_threshold
    is_battery_filled = current_battery_percent >= battery_high_threshold
    is_battery_low = current_battery_percent < min_battery_percent

    # Implementation of the truth table from the image
    # G | S | BF | State
    # ------------------
    # 0 | 0 | 0  | 3  (Grid demand low, Solar low, Battery low -> Use grid)
    # 0 | 0 | 1  | 0  (Not in table, but logically: Grid demand low, Solar low, Battery high -> Use battery)
    # 0 | 1 | 0  | 1  (Grid demand low, Solar high, Battery low -> Charge battery)
    # 0 | 1 | 1  | 0  (Grid demand low, Solar high, Battery high -> Use solar)
    # 1 | 0 | 0  | 3  (Grid demand high, Solar low, Battery low -> Use grid)
    # 1 | 0 | 1  | 2  (Grid demand high, Solar low, Battery high -> Use battery)
    # 1 | 1 | 0  | 1  (Grid demand high, Solar high, Battery low -> Charge battery)
    # 1 | 1 | 1  | 0  (Grid demand high, Solar high, Battery high -> Use solar)

    # Logic implementation based on the truth table and requirements
    if is_solar_production_high:
        if is_battery_filled:
            return 0
        else:
            return 1
    else:
        # Solar production is low
        if is_battery_low or not is_grid_demand_high:
            return 3
        else:
            return 2


# USAGE
# """
# Function to get grid demand from Stromgedacht API based on zip code

# Args:
#     zip_code (str): The postal code to check grid demand for
    
# Returns:
#     int: Grid demand value (0=low, 1=medium, 2=high)
# """
# def get_grid_demand_from_api(zip_code):
#     # Placeholder for actual API call to Stromgedacht
#     # In a real implementation, you would make an HTTP request like:
#     # response = requests.get(f"https://api.stromgedacht.de/v1/now?zip={zip_code}")
#     # return response.json()["state"]
    
#     # For testing purposes, return a random value between 0-2
#     import random
#     return random.randint(0, 2)
# 
# 
# """
# Get user input for system configuration and run the algorithm

# Returns:
#     None: Displays recommendation to the user
# """
