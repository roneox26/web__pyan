import sqlite3

conn = sqlite3.connect('instance/ngo.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE customers ADD COLUMN welfare_fee REAL DEFAULT 0.0")
    conn.commit()
    print("welfare_fee column added successfully!")
except Exception as e:
    print(f"Column might already exist or error: {e}")

conn.close()
