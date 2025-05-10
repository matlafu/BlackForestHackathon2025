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
BATTERY_HIGH_THRESHOLD = 0.80



def determine_balkonsolar_state(
    grid_demand,
    solar_production,
    current_battery_percent, # we get this from moritz, 
    # from the virtual battery class, in percentage
    max_solar_capacity,
    max_battery_percent, # we get this from user
    min_battery_percent # we get this from user
):
    # Define thresholds for solar production (high if > 50% of maximum capacity)
    solar_high_threshold = USER_SOLAR_HIGH_THRESHOLD * max_solar_capacity
    
    # Convert raw values to binary states
    is_grid_demand_high = grid_demand > STROMGEDACHT_HIGH_THRESHOLD  # Stromgedacht API: 0=low, 1 or 2=high
    is_solar_production_high = solar_production > solar_high_threshold
    is_battery_filled = current_battery_percent >= BATTERY_HIGH_THRESHOLD * max_battery_percent  # 90% threshold
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
            return 0  # Use solar to power household
        else:
            return 1  # Charge battery from solar
    else:
        # Solar production is low
        if is_battery_low or not is_grid_demand_high:
            return 3  # Use grid to power household
        else:
            return 2  # Use battery to power household


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
# def run_balkonsolar_advisor():
#     # Get user inputs with reasonable defaults
#     print("===== Balkonsolar System Advisor =====")
    
#     try:
#         # User inputs for system configuration
#         zip_code = input("Enter your ZIP code (e.g., 10115): ") or "10115"
#         max_solar_capacity = float(input("Enter maximum solar production capacity in Watts (e.g., 800): ") or "800")
#         max_battery_capacity = float(input("Enter maximum battery capacity in Wh (e.g., 1200): ") or "1200")
        
#         # Derive reasonable defaults for minimum battery threshold (25% of max)
#         min_battery_threshold = float(input(f"Enter minimum battery threshold in Wh (default: {int(0.25 * max_battery_capacity)}): ") 
#                                 or str(0.25 * max_battery_capacity))
        
#         # For demonstration purposes, simulate current values
#         # In a real implementation, you would fetch these from sensors or APIs
#         current_solar_production = float(input("Enter current solar production in Watts (e.g., 500): ") or "500")
#         current_battery_capacity = float(input("Enter current battery capacity in Wh (e.g., 600): ") or "600")
        
#         # Get grid demand from API based on zip code
#         print(f"\nFetching grid demand data for ZIP code {zip_code}...")
#         current_grid_demand = get_grid_demand_from_api(zip_code)
#         grid_status = ["Low", "Medium", "High"][current_grid_demand]
#         print(f"Current grid demand: {grid_status}")
        
#         # Determine optimal system state
#         state = determine_balkonsolar_state(
#             current_grid_demand,
#             current_solar_production,
#             current_battery_capacity,
#             max_solar_capacity,
#             max_battery_capacity,
#             min_battery_threshold
#         )
        
#         # Map state number to human-readable description
#         state_descriptions = [
#             "Use solar to power household",
#             "Charge battery from solar",
#             "Use battery to power household",
#             "Use grid to power household"
#         ]
        
#         # Display system status and recommendation
#         print("\n===== System Status =====")
#         print(f"Solar Production: {current_solar_production}W / {max_solar_capacity}W")
#         print(f"Battery Capacity: {current_battery_capacity}Wh / {max_battery_capacity}Wh " + 
#               f"({int(current_battery_capacity/max_battery_capacity*100)}%)")
        
#         print("\n===== Recommendation =====")
#         print(f"Optimal state: {state_descriptions[state]}")
        
#     except ValueError as e:
#         print(f"Error processing input: {e}")
#         print("Please enter valid numeric values.")


# # If this file is run directly, start the advisor
# if __name__ == "__main__":
#     run_balkonsolar_advisor()
