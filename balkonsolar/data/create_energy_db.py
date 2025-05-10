import sqlite3
import os

def create_energy_database(db_path="balkonsolar/data/energy_data.db"):
    """Create a SQLite database with tables for energy monitoring"""
    
    # Ensure directory exists if needed
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Connect to database (will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    tables = [
        # Solar output table
        """
        CREATE TABLE IF NOT EXISTS solar_output (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            value REAL NOT NULL
        )
        """,
        
        # Battery storage status table
        """
        CREATE TABLE IF NOT EXISTS battery_storage_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            value REAL NOT NULL
        )
        """,
        
        # Grid usage table
        """
        CREATE TABLE IF NOT EXISTS grid_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            value REAL NOT NULL
        )
        """,
        
        # Output algorithm table
        """
        CREATE TABLE IF NOT EXISTS output_algorithm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            value REAL NOT NULL
        )
        """,
        """
            CREATE TABLE IF NOT EXISTS irradiation_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                value REAL NOT NULL
            )
            """
    ]
    
    # Execute each table creation query
    for table_query in tables:
        cursor.execute(table_query)
    
    # Create indexes for faster timestamp queries
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_solar_tstamp ON solar_output(tstamp)",
        "CREATE INDEX IF NOT EXISTS idx_battery_tstamp ON battery_storage_status(tstamp)",
        "CREATE INDEX IF NOT EXISTS idx_grid_tstamp ON grid_usage(tstamp)",
        "CREATE INDEX IF NOT EXISTS idx_algo_tstamp ON output_algorithm(tstamp)",
        "CREATE INDEX IF NOT EXISTS idx_irradiation_tstamp ON irradiation_data(tstamp)"
    ]
    
    for index_query in indexes:
        cursor.execute(index_query)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")
    print("Tables created: solar_output, battery_storage_status, grid_usage, output_algorithm")

if __name__ == "__main__":
    create_energy_database() 