import pandas as pd
from datetime import datetime, timedelta
import os

"""
Utility for reading and processing average energy consumption data from Excel for Balkonsolar scheduling.

Provides functions to aggregate, extract, and retrieve 24-hour energy usage profiles for use in forecasting and simulation.
"""

def aggregate_to_hourly_preserve_columns(df):
    """
    Aggregate a DataFrame to hourly means, preserving all columns except the timestamp.

    Args:
        df (pd.DataFrame): Input DataFrame with a 'Tstamp_Tstamp' column.

    Returns:
        pd.DataFrame: DataFrame indexed by hour with mean values for each column.
    """
    # Make a copy of the dataframe
    df_copy = df.copy()

    # Create a new column for the hour
    df_copy['Hour'] = df_copy['Tstamp_Tstamp'].str.extract(r'(\d{2}):', expand=False)

    # Group by the hour and calculate mean for all columns except Tstamp_Tstamp
    numeric_cols = df_copy.columns.drop(['Tstamp_Tstamp', 'Hour'])
    result = df_copy.groupby('Hour')[numeric_cols].mean()

    # Format the index better
    result.index = [f"{hour}:00" for hour in result.index]

    return result

def get_values_for_next_24h(df, start_datetime, german_holidays=None):
    """
    Get values for the next 24 hours starting from start_datetime.

    Args:
        df (pd.DataFrame): DataFrame with hourly values indexed by HH:00.
        start_datetime (datetime): Starting datetime.
        german_holidays: (Unused, for future extension).

    Returns:
        list: 24 values representing the next 24 hours.
    """

    values = []

    # Loop through the next 24 hours
    for hour_offset in range(24):
        # Calculate the current datetime in the sequence
        current_dt = start_datetime + timedelta(hours=hour_offset)

        # Determine day type
        if current_dt.weekday() == 5:  # Saturday (0=Monday, 5=Saturday)
            day_type = "SA"
        else:
            day_type = "WT"  # Weekday

        # Format the month part of the column name (always 2012 year)
        month_str = f"2012-{current_dt.month:02d}-01"

        # Build the full column name
        column_name = f"{month_str}_{day_type}"

        # Get the hour for the row lookup
        hour_key = f"{current_dt.hour:02d}:00"

        # Try to get the value
        try:
            if column_name in df.columns and hour_key in df.index:
                value = df.loc[hour_key, column_name]
                values.append(value)
            else:
                # If hour or column not found, append None or a default value
                values.append(None)
        except Exception as e:
            print(f"Error getting value for {current_dt}: {e}")
            values.append(None)

    return values

def get_excel_data() -> pd.DataFrame:
    """
    Load and process the standard energy consumption Excel file.

    Returns:
        pd.DataFrame: DataFrame with combined headers and cleaned data.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "StandardStromVerbrauch.xlsx")
    df = pd.read_excel(excel_path, header=None)
    # Extract the header rows
    first_header = df.iloc[0]
    second_header = df.iloc[1]

    # Combine the headers
    combined_headers = [f"{str(h1)[:10]}_{h2}" for h1, h2 in zip(first_header, second_header)]

    # Set the combined headers and remove the header rows
    df = df.iloc[2:]  # Skip the first two rows
    df.columns = combined_headers

    # Reset the index
    df = df.reset_index(drop=True)

    return df


def main(tstamp: datetime) -> list[float]|None:
    """
    Get the values for the next 24 hours starting from tstamp.

    Args:
        tstamp (datetime): Starting datetime for the 24-hour window.

    Returns:
        list[float] or None: List of 24 hourly values, or None on error.
    """
    try:
        base_df = get_excel_data()
        hourly_df = aggregate_to_hourly_preserve_columns(base_df)
        return get_values_for_next_24h(hourly_df, tstamp)
    except Exception as e:
        print(f"Error getting values for {tstamp}: {e}")
        return None
if __name__ == "__main__":
    main(datetime.now())
