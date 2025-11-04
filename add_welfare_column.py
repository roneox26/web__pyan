import sqlite3
import os

db_path = 'instance/loan.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE customers ADD COLUMN welfare_fee REAL DEFAULT 0.0")
        conn.commit()
        print("welfare_fee column added to customers table!")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
            print("welfare_fee column already exists")
        else:
            print(f"Error: {e}")
    
    conn.close()
else:
    print(f"Database not found at {db_path}")
