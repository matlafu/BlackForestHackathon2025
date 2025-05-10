import sqlite3
import os
import datetime
from typing import Optional, Dict, List, Any

class DatabaseManager:
    """
    Standalone database manager for AppDaemon apps
    Can be used without requiring the main balkonsolar package
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the database manager
        
        Args:
            db_path: Path to the database file
        """
        if db_path is None:
            # Try multiple paths in order of preference
            
            # 1. First try repository root (local development setup)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up two levels: from apps dir to appdaemon dir to balkonsolar dir
            root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
            # Use a data directory at the balkonsolar root
            data_dir = os.path.join(root_dir, "data")
            repo_db_path = os.path.join(data_dir, "energy_data.db")
            
            if os.path.exists(repo_db_path) or self._can_create_path(repo_db_path):
                db_path = repo_db_path
                print(f"Using local development database at: {db_path}")
            
            # 2. If not found, check for AppDaemon config-relative path (container setup)
            elif os.path.exists('/config'):
                config_db_path = "/config/balkonsolar/data/energy_data.db"
                if os.path.exists(config_db_path) or self._can_create_path(config_db_path):
                    db_path = config_db_path
                    print(f"Using container database at: {db_path}")
            
            # 3. Fallback to user's home directory
            if db_path is None:
                home_dir = os.path.expanduser("~")
                db_path = os.path.join(home_dir, "energy_data.db")
                print(f"Using fallback database at: {db_path}")
        else:
            # Handle relative paths
            if not os.path.isabs(db_path):
                # Convert relative path from apps directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.abspath(os.path.join(current_dir, db_path))
            print(f"Using specified database at: {db_path}")
            
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _can_create_path(self, path: str) -> bool:
        """Check if we can create the directory structure for this path"""
        try:
            dir_path = os.path.dirname(path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            return True
        except (OSError, PermissionError):
            return False
    
    def _ensure_db_exists(self):
        """Make sure the database exists and has the required tables"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir)
                print(f"Created database directory: {db_dir}")
            except Exception as e:
                print(f"Warning: Could not create database directory: {e}")
                # Try user's home directory as fallback
                home_dir = os.path.expanduser("~")
                self.db_path = os.path.join(home_dir, "energy_data.db")
                print(f"Falling back to home directory database: {self.db_path}")
                
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        tables = [
            # Table for battery storage status
            """
            CREATE TABLE IF NOT EXISTS battery_storage_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                value REAL NOT NULL
            )
            """,
            
            # Table for solar output
            """
            CREATE TABLE IF NOT EXISTS solar_output (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                value REAL NOT NULL
            )
            """,
            
            # Table for grid usage
            """
            CREATE TABLE IF NOT EXISTS grid_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                value REAL NOT NULL
            )
            """
        ]
        
        for table_query in tables:
            cursor.execute(table_query)
            
        conn.commit()
        conn.close()
        
    def _get_connection(self):
        """Get a database connection with row factory enabled"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
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
    
    def store_battery_status(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store battery status value"""
        return self.store_value("battery_storage_status", value, timestamp)
    
    def store_solar_output(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store solar output value"""
        return self.store_value("solar_output", value, timestamp)
    
    def store_grid_usage(self, value: float, timestamp: Optional[str] = None) -> bool:
        """Store grid usage value"""
        return self.store_value("grid_usage", value, timestamp)
    
    def get_latest_values(self, table: str, limit: int = 1) -> List[Dict[str, Any]]:
        """
        Get the latest values from a specific table
        
        Args:
            table: Table name
            limit: Number of records to retrieve
            
        Returns:
            List of records as dictionaries
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                f"SELECT id, tstamp, value FROM {table} ORDER BY tstamp DESC LIMIT ?",
                (limit,)
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
            print(f"Error getting values from {table}: {e}")
            return []
    
    def get_battery_status(self, limit: int = 1) -> List[Dict[str, Any]]:
        """Get the latest battery status entries"""
        return self.get_latest_values("battery_storage_status", limit)
    
    def get_solar_output(self, limit: int = 1) -> List[Dict[str, Any]]:
        """Get the latest solar output entries"""
        return self.get_latest_values("solar_output", limit)
    
    def get_grid_usage(self, limit: int = 1) -> List[Dict[str, Any]]:
        """Get the latest grid usage entries"""
        return self.get_latest_values("grid_usage", limit)
    
    def get_values_by_timeframe(self, table: str, start_time: str, end_time: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get values from a specific table within a timeframe
        
        Args:
            table: Table name
            start_time: Start time in ISO format
            end_time: Optional end time in ISO format
            limit: Maximum number of records to retrieve
            
        Returns:
            List of records as dictionaries
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if end_time:
                cursor.execute(
                    f"SELECT id, tstamp, value FROM {table} WHERE tstamp BETWEEN ? AND ? ORDER BY tstamp DESC LIMIT ?",
                    (start_time, end_time, limit)
                )
            else:
                cursor.execute(
                    f"SELECT id, tstamp, value FROM {table} WHERE tstamp >= ? ORDER BY tstamp DESC LIMIT ?",
                    (start_time, limit)
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
            print(f"Error getting values by timeframe from {table}: {e}")
            return [] 