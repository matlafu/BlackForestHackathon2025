import sqlite3
import datetime
from typing import List, Dict, Union, Tuple, Optional

"""
Utility class for interacting with the Balkonsolar energy monitoring SQLite database.

Provides methods to store and retrieve solar, battery, grid, and algorithm output data for testing, prototyping, or alternative workflows.
"""

class EnergyDB:
    """
    Utility class for interacting with the energy monitoring database.
    Provides methods to store and retrieve solar, battery, grid, and algorithm output data.
    """

    def __init__(self, db_path: str = "energy_data.db"):
        """
        Initialize the EnergyDB interface.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path

    def store_solar_output(self, value: float, timestamp: Optional[str] = None) -> bool:
        return self._store_value("solar_output", value, timestamp)

    def store_battery_status(self, value: float, timestamp: Optional[str] = None) -> bool:
        return self._store_value("battery_storage_status", value, timestamp)

    def store_grid_usage(self, value: float, timestamp: Optional[str] = None) -> bool:
        return self._store_value("grid_usage", value, timestamp)

    def store_algorithm_output(self, value: float, timestamp: Optional[str] = None) -> bool:
        return self._store_value("output_algorithm", value, timestamp)

    def _store_value(self, table: str, value: float, timestamp: Optional[str] = None) -> bool:
        """
        Store a value in the specified table, optionally with a timestamp.

        Args:
            table (str): Table name.
            value (float): Value to store.
            timestamp (str, optional): Timestamp string. If None, uses current time.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if timestamp:
                query = f"INSERT INTO {table} (tstamp, value) VALUES (?, ?)"
                cursor.execute(query, (timestamp, value))
            else:
                query = f"INSERT INTO {table} (value) VALUES (?)"
                cursor.execute(query, (value,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing value in {table}: {e}")
            return False

    def get_data(self, table: str, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        """
        Retrieve data from a table, optionally filtered by time range and limited in count.

        Args:
            table (str): Table name.
            limit (int): Maximum number of records to return.
            start_time (str, optional): Start time (inclusive) for filtering.
            end_time (str, optional): End time (inclusive) for filtering.

        Returns:
            List[Dict]: List of records as dictionaries.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = f"SELECT id, tstamp, value FROM {table}"
            params = []
            if start_time or end_time:
                query += " WHERE"
                if start_time:
                    query += " tstamp >= ?"
                    params.append(start_time)
                if end_time:
                    if start_time:
                        query += " AND"
                    query += " tstamp <= ?"
                    params.append(end_time)
            query += " ORDER BY tstamp DESC LIMIT ?"
            params.append(limit)
            cursor.execute(query, params)
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
            print(f"Error querying {table}: {e}")
            return []

    def get_latest_data(self, table: str) -> Dict:
        """
        Retrieve the latest record from a table.

        Args:
            table (str): Table name.

        Returns:
            Dict: Latest record as a dictionary, or None if not found.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = f"SELECT id, tstamp, value FROM {table} ORDER BY tstamp DESC LIMIT 1"
            cursor.execute(query)
            row = cursor.fetchone()
            conn.close()
            return {
                "id": row["id"],
                "timestamp": row["tstamp"],
                "value": row["value"]
            } if row else None
        except Exception as e:
            print(f"Error getting latest data from {table}: {e}")
            return None

    def get_solar_output(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        return self.get_data("solar_output", limit, start_time, end_time)

    def get_battery_status(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        return self.get_data("battery_storage_status", limit, start_time, end_time)

    def get_grid_usage(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        return self.get_data("grid_usage", limit, start_time, end_time)

    def get_algorithm_output(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        return self.get_data("output_algorithm", limit, start_time, end_time)

    def close(self):
        """
        Placeholder for closing persistent connections (not used).
        """
        pass  # No persistent connection to close

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit (no persistent connection to close).
        """
        pass  # No persistent connection to close
