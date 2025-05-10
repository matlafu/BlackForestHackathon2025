import sqlite3
import os
from datetime import datetime, timedelta

def get_default_db_path():
    """Get the default database path"""
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, "energy_data.db")

def query_table(db_path, table_name, limit=10):
    """Query a table from the database and print results"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Get the data
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    
    # Print the table
    print(f"\n=== {table_name.upper()} (last {limit} records) ===")
    print(" | ".join(columns))
    print("-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1)))
    
    for row in rows:
        print(" | ".join(str(val) for val in row))
    
    # Count total records
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"\nTotal records in {table_name}: {count}")
    
    conn.close()

def get_data_by_date_range(db_path, table_name, start_date, end_date):
    """Query data from a specific date range"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Get the data for the date range
    cursor.execute(f"SELECT * FROM {table_name} WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp",
                  (start_date, end_date))
    rows = cursor.fetchall()
    
    # Print the table
    print(f"\n=== {table_name.upper()} ({start_date} to {end_date}) ===")
    print(" | ".join(columns))
    print("-" * (sum(len(col) for col in columns) + 3 * (len(columns) - 1)))
    
    for row in rows:
        print(" | ".join(str(val) for val in row))
    
    print(f"\nFound {len(rows)} records in the specified date range")
    
    conn.close()

def main():
    # Get the database path
    db_path = input(f"Enter database path (press Enter for default {get_default_db_path()}): ")
    if not db_path:
        db_path = get_default_db_path()
    
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return
    
    print(f"Using database at: {db_path}")
    
    # Connect to the database to get table names
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    
    if not tables:
        print("No tables found in the database.")
        return
    
    print("\nAvailable tables:")
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table}")
    
    while True:
        print("\nOptions:")
        print("1. View recent records from a table")
        print("2. View records by date range")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            table_idx = int(input(f"Enter table number (1-{len(tables)}): ")) - 1
            if 0 <= table_idx < len(tables):
                limit = int(input("Enter number of recent records to show: ") or "10")
                query_table(db_path, tables[table_idx], limit)
            else:
                print("Invalid table number.")
        
        elif choice == "2":
            table_idx = int(input(f"Enter table number (1-{len(tables)}): ")) - 1
            if 0 <= table_idx < len(tables):
                today = datetime.now().strftime("%Y-%m-%d")
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                
                start_date = input(f"Enter start date (YYYY-MM-DD) [default: {yesterday}]: ")
                if not start_date:
                    start_date = yesterday
                
                end_date = input(f"Enter end date (YYYY-MM-DD) [default: {today}]: ")
                if not end_date:
                    end_date = today
                
                # Add time to make the range inclusive
                if len(start_date) == 10:  # Just the date
                    start_date += " 00:00:00"
                if len(end_date) == 10:  # Just the date
                    end_date += " 23:59:59"
                
                get_data_by_date_range(db_path, tables[table_idx], start_date, end_date)
            else:
                print("Invalid table number.")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 