import sqlite3
import os
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd

class DatabaseInterface:
    """
    Interface for accessing energy data from the shared database
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database interface
        
        Args:
            db_path: Optional path to the database. If None, tries to find the default path.
        """
        if db_path is None:
            # Try to find the database in common locations
            root_dir = Path(__file__).parent.parent  # balkonsolar directory
            default_path = os.path.join(root_dir, "data", "energy_data.db")
            
            possible_paths = [
                default_path,
                "energy_data.db",
                os.path.join("data", "energy_data.db"),
                os.path.join("balkonsolar", "data", "energy_data.db"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "energy_data.db"),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    db_path = path
                    break
            
            if db_path is None:
                # If no existing database found, use the default location
                db_path = default_path
                # Ensure data directory exists
                data_dir = os.path.dirname(default_path)
                os.makedirs(data_dir, exist_ok=True)
        
        self.db_path = db_path
        print(f"DatabaseInterface initialized with database at: {self.db_path}")

    def _get_connection(self):
        """Get a database connection with row factory enabled"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_latest_value(self, table: str) -> Optional[Dict[str, Any]]:
        """
        Get the latest value from a specific table
        
        Args:
            table: Table name
            
        Returns:
            Dictionary with the latest record or None if no data
        """
        try:
            if not os.path.exists(self.db_path):
                return None
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # First check if the table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                conn.close()
                return None
            
            cursor.execute(
                f"SELECT id, tstamp, value FROM {table} ORDER BY tstamp DESC LIMIT 1"
            )
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "id": row["id"],
                    "timestamp": row["tstamp"],
                    "value": row["value"]
                }
            
            return None
        except Exception as e:
            print(f"Error getting latest value from {table}: {e}")
            return None
    
    def get_battery_status(self) -> Dict[str, str]:
        """
        Get the current battery status
        
        Returns:
            Dictionary with battery status
        """
        result = self.get_latest_value("battery_storage_status")
        
        if result:
            charge = result["value"]
            
            return {
                "current_charge_kwh": charge,
                "timestamp": result["timestamp"]
            }
        else:
            # Return default values if no data
            return {
                "current_charge_kwh": 0.0,
                "timestamp": datetime.datetime.now().isoformat()
            }
    
    def get_solar_output(self) -> float:
        """
        Get the latest solar output value
        
        Returns:
            Latest solar output value or 0.0 if no data
        """
        result = self.get_latest_value("solar_output")
        return result["value"] if result else 0.0
    
    def get_grid_usage(self) -> float:
        """
        Get the latest grid usage value
        
        Returns:
            Latest grid usage value or 0.0 if no data
        """
        result = self.get_latest_value("grid_usage")
        return result["value"] if result else 0.0
    
    def get_history(self, table: str, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get history for a specific table
        
        Args:
            table: Table name
            hours: Number of hours to look back
            
        Returns:
            List of records
        """
        try:
            if not os.path.exists(self.db_path):
                return []
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # First check if the table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                conn.close()
                return []
            
            # Calculate the timestamp for the start of the period
            start_time = (datetime.datetime.now() - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                f"SELECT id, tstamp, value FROM {table} WHERE tstamp >= ? ORDER BY tstamp DESC",
                (start_time,)
            )
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row["id"],
                    "timestamp": row["tstamp"],
                    "value": row["value"]
                })
            
            conn.close()
            return results
        except Exception as e:
            print(f"Error getting history from {table}: {e}")
            return []
    
    def get_battery_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get battery history"""
        results = self.get_history("battery_storage_status", hours)
        
        # Calculate percentage based on capacity
        capacity = 2.56  # kWh
        for item in results:
            item["capacity_kwh"] = capacity
            item["percent_full"] = min(100, max(0, (item["value"] / capacity) * 100))
            item["current_charge_kwh"] = item["value"]
            
        return results
    
    def get_solar_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get solar output history"""
        return self.get_history("solar_output", hours)
    
    def get_grid_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get grid usage history"""
        return self.get_history("grid_usage", hours) 
    
    def store_value(self, table: str, value: float, timestamp: Optional[str] = None) -> bool:
        """
        Store a value in a specific table
        
        Args:
            table: Table name
            value: Value to store
            timestamp: Optional timestamp (if None, current time is used)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if timestamp:
                cursor.execute(
                    f"INSERT INTO {table} (tstamp, value) VALUES (?, ?)",
                    (timestamp, value)
                )
            else:
                cursor.execute(
                    f"INSERT INTO {table} (value) VALUES (?)",
                    (value,)
                )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing value in {table}: {e}")
            return False
        
    def store_irradiation_data(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store irradiation data value"""
        return self.store_value("irradiation_data", value, timestamp)
    
    def store_output_algorithm(self, df, timestamp_column: Optional[str] = None) -> bool:
        """
        Replace output_algorithm table with contents of DataFrame
        
        Args:
            df: DataFrame containing the data to store
            timestamp_column: Optional column name for timestamp data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            if timestamp_column and timestamp_column in df.columns:
                df = df.rename(columns={timestamp_column: "tstamp"})
            df.to_sql("output_algorithm", conn, if_exists="replace", index=False)
            conn.close()
            return True
        except Exception as e:
            print(f"Error replacing output_algorithm table: {e}")
            return False
