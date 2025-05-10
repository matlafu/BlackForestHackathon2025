import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from balkonsolar.core.database_interface import DatabaseInterface

# Create a mock DataFrame for the next 24 hours
hours = pd.date_range(start=datetime.now().replace(minute=0, second=0, microsecond=0), periods=24, freq='H')
np.random.seed(42)

# Simulated data
pv_prod = np.random.randint(100, 400, size=24)  # in Wh
grid_demand = np.random.choice([-1, 1, 2, 3], size=24, p=[0.2, 0.4, 0.3, 0.1])
usage = np.random.randint(50, 250, size=24)  # in Wh
battery_input = np.zeros(24)  # initialized to 0

# Create the DataFrame
df = pd.DataFrame({
    "pv_prod": pv_prod,
    "grid_demand": grid_demand,
    "usage": usage,
    "battery_input": battery_input
}, index=hours)

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
for idx, row in df.sort_values(by=["grid_demand", "surplus"], ascending=[True, False]).iterrows():
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

db = DatabaseInterface()
db.store_output_algorithm(df)