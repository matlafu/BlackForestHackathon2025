import sqlite3
import datetime
from typing import List, Dict, Union, Tuple, Optional

class EnergyDB:
    """Utility class for interacting with the energy monitoring database"""
    
    def __init__(self, db_path: str = "energy_data.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
    
    def _connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        # Enable row factory to get dictionary-like results
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def store_solar_output(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store solar output value"""
        return self._store_value("solar_output", value, timestamp)
    
    def store_battery_status(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store battery storage status value"""
        return self._store_value("battery_storage_status", value, timestamp)
    
    def store_grid_usage(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store grid usage value"""
        return self._store_value("grid_usage", value, timestamp)
    
    def store_algorithm_output(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store algorithm output value"""
        return self._store_value("output_algorithm", value, timestamp)
    
    def _store_value(self, table: str, value: float, timestamp: Optional[str] = None) -> bool:
        """Store a value in the specified table"""
        try:
            if timestamp:
                query = f"INSERT INTO {table} (tstamp, value) VALUES (?, ?)"
                self.cursor.execute(query, (timestamp, value))
            else:
                query = f"INSERT INTO {table} (value) VALUES (?)"
                self.cursor.execute(query, (value,))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error storing value in {table}: {e}")
            return False
    
    def get_data(self, table: str, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        """
        Get data from a specific table with optional time filtering
        
        Args:
            table: Table name to query
            limit: Maximum number of records to return
            start_time: Optional start time in ISO format (YYYY-MM-DD HH:MM:SS)
            end_time: Optional end time in ISO format (YYYY-MM-DD HH:MM:SS)
            
        Returns:
            List of records as dictionaries
        """
        try:
            query = f"SELECT id, tstamp, value FROM {table}"
            params = []
            
            # Add time filters if provided
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
            
            # Add ordering and limit
            query += " ORDER BY tstamp DESC LIMIT ?"
            params.append(limit)
            
            # Execute query
            self.cursor.execute(query, params)
            
            # Convert rows to dictionaries
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    "id": row["id"],
                    "timestamp": row["tstamp"],
                    "value": row["value"]
                })
                
            return results
        except Exception as e:
            print(f"Error querying {table}: {e}")
            return []
    
    def get_latest_data(self, table: str) -> Dict:
        """Get the latest data from a specific table"""
        try:
            query = f"SELECT id, tstamp, value FROM {table} ORDER BY tstamp DESC LIMIT 1"
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            return {
                "id": row["id"],
                "timestamp": row["tstamp"],
                "value": row["value"]
            }
        except Exception as e:
            print(f"Error getting latest data from {table}: {e}")
            return None
    
    def get_solar_output(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        """Get solar output data"""
        return self.get_data("solar_output", limit, start_time, end_time)
    
    def get_battery_status(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        """Get battery storage status data"""
        return self.get_data("battery_storage_status", limit, start_time, end_time)
    
    def get_grid_usage(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        """Get grid usage data"""
        return self.get_data("grid_usage", limit, start_time, end_time)
    
    def get_algorithm_output(self, limit: int = 100, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[Dict]:
        """Get algorithm output data"""
        return self.get_data("output_algorithm", limit, start_time, end_time)
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            
    def __enter__(self):
        """Support for context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting context"""
        self.close() 