#!/usr/bin/env python3
"""
Example script demonstrating how to use the energy database
"""

import time
import random
import datetime
from balkonsolar.data.create_energy_db import create_energy_database
from balkonsolar.database_shenanigans.energy_db import EnergyDB

def add_sample_data():
    """Add some sample data to the database"""
    # Initialize the database
    db = EnergyDB()
    
    # Current time
    now = datetime.datetime.now()
    
    # Add 24 hours of simulated data at 15-minute intervals
    for i in range(96):  # 24 hours * 4 intervals per hour
        # Calculate timestamp (going backward from now)
        timestamp = (now - datetime.timedelta(minutes=15 * i)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate random values
        solar = random.uniform(0, 5.0) if 8 <= now.hour <= 20 else random.uniform(0, 0.1)
        battery = random.uniform(20, 95)
        grid = random.uniform(-2.0, 3.0)  # Negative means sending to grid
        algorithm = random.choice([0, 1, 2, 3])  # Different modes
        
        # Store in database
        db.store_solar_output(solar, timestamp)
        db.store_battery_status(battery, timestamp)
        db.store_grid_usage(grid, timestamp)
        db.store_algorithm_output(algorithm, timestamp)
        
    db.close()
    print(f"Added 96 sample data points (24 hours of 15-minute intervals)")

def query_and_display():
    """Query and display data from the database"""
    db = EnergyDB()
    
    # Get the most recent data
    solar_data = db.get_solar_output(limit=5)
    battery_data = db.get_battery_status(limit=5)
    grid_data = db.get_grid_usage(limit=5)
    algorithm_data = db.get_algorithm_output(limit=5)
    
    # Display the data
    print("\nMost recent solar output data:")
    for entry in solar_data:
        print(f"  {entry['timestamp']}: {entry['value']:.2f} kW")
    
    print("\nMost recent battery status data:")
    for entry in battery_data:
        print(f"  {entry['timestamp']}: {entry['value']:.2f}%")
    
    print("\nMost recent grid usage data:")
    for entry in grid_data:
        direction = "from grid" if entry['value'] > 0 else "to grid"
        print(f"  {entry['timestamp']}: {abs(entry['value']):.2f} kW {direction}")
    
    print("\nMost recent algorithm output data:")
    for entry in algorithm_data:
        mode = ["Off", "Solar Priority", "Grid Priority", "Battery Priority"][int(entry['value'])]
        print(f"  {entry['timestamp']}: Mode {int(entry['value'])} ({mode})")
    
    # Get data from a specific time range
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"\nSolar output for {yesterday}:")
    day_data = db.get_solar_output(
        start_time=f"{yesterday} 00:00:00", 
        end_time=f"{yesterday} 23:59:59",
        limit=100
    )
    for entry in day_data:
        print(f"  {entry['timestamp']}: {entry['value']:.2f} kW")
    
    db.close()

if __name__ == "__main__":
    # Check if the database exists, if not create it
    try:
        with EnergyDB() as db:
            pass
    except:
        print("Creating new database...")
        create_energy_database()
    
    # Add sample data
    add_sample_data()
    
    # Query and display data
    query_and_display() 