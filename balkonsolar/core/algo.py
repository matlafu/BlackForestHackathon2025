import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Fix imports: use relative import for database_interface
from database_interface import DatabaseInterface

# Add the project root to the Python path - keep this as a backup
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Use relative import for read_average_energy_consumption
from utils.read_average_energy_consumption import main as read_average_energy_consumption

# Initialize database interface
db = DatabaseInterface()

# Get irradiation forecast
irradiation_forecast = db.get_irradiation_forecast()
irradiation_forecast["timestamp"] = pd.to_datetime(irradiation_forecast["timestamp"])
irradiation_forecast = irradiation_forecast[irradiation_forecast["timestamp"].apply(lambda x: x.minute == 0 and x.second == 0)]
# Set the timestamp as index
irradiation_forecast = irradiation_forecast.set_index("timestamp")
irradiation_forecast = irradiation_forecast.rename(columns={"watt_hours": "pv_prod"})


# Get grid usage forecast
grid_usage_forecast = db.get_grid_usage_forecast()
grid_usage_forecast["timestamp"] = grid_usage_forecast["timestamp"].apply(lambda x: datetime.strptime(x.replace("+02:00", ""), "%Y-%m-%d %H:%M:%S"))
# Set the timestamp as index
grid_usage_forecast = grid_usage_forecast.set_index("timestamp")

# Get average grid usage for the next 24 hours
average_grid_usage = read_average_energy_consumption(datetime.now())

# Create a mock DataFrame for the next 24 hours
hours = pd.date_range(start=datetime.now().replace(minute=0, second=0, microsecond=0), periods=24, freq='h')
np.random.seed(42)

# Simulated data bc out battery is not working and our pv is also not genearting any power so our virtual battery is empty lol
battery_input = np.zeros(24)  # initialized to 0

# Create the DataFrame
df = pd.DataFrame({
    "usage": average_grid_usage,
    "battery_input": battery_input,
}, index=hours)

# Merge irradiation forecast with df
df = pd.merge(df, irradiation_forecast, left_index=True, right_index=True, how="left")


# Merge grid usage forecast with df
df = pd.merge(df, grid_usage_forecast, left_index=True, right_index=True, how="left")
# Fill the missing values with 0
df["grid_state"] = df["grid_state"].fillna(0)
df["pv_prod"] = df["pv_prod"].fillna(0)

# Set battery capacity values
battery_max = 2000  # Wh
battery_current = 1500  # Wh
battery_needed = battery_max - battery_current

# Add helper column for sorting: surplus = pv_prod - usage
df["surplus"] = df["pv_prod"] - df["usage"]

# Initialize suggested_state column
df["suggested_state"] = "use grid"

# Copy battery_needed
remaining_to_charge = battery_needed

# Charging phase: prioritize hours for charging
for idx, row in df.sort_values(by=["grid_state", "surplus"], ascending=[True, False]).iterrows():
    if remaining_to_charge <= 0:
        break

    if row["surplus"] <= 0:
        continue  # skip if no surplus to charge from

    charge_amount = min(row["surplus"], remaining_to_charge)

    # Update battery input
    df.at[idx, "battery_input"] = charge_amount

    # Determine state
    if row["surplus"] > charge_amount:
        df.at[idx, "suggested_state"] = "mixed"
    else:
        df.at[idx, "suggested_state"] = "charge battery"

    remaining_to_charge -= charge_amount

# Utilization phase: recommend solar usage if still surplus exists
for idx, row in df.iterrows():
    if row["suggested_state"] != "use grid":
        continue  # already marked

    if row["surplus"] > 0:
        df.at[idx, "suggested_state"] = "power the household from solar"

# Drop helper column before presenting
df.drop(columns=["surplus"], inplace=True)

# Transform the index to a column 
df.reset_index(inplace=True)
df.rename(columns={"index": "timestamp"}, inplace=True)

# Store the output
db.store_output_algorithm(df)