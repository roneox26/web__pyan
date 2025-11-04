import sqlite3

conn = sqlite3.connect('instance/loan.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE loans ADD COLUMN welfare_fee REAL DEFAULT 0.0")
    conn.commit()
    print("Column 'welfare_fee' added successfully!")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
finally:
    conn.close()
