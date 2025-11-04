import sqlite3

conn = sqlite3.connect('instance/loan.db')
cursor = conn.cursor()

try:
    cursor.execute("UPDATE customers SET welfare_fee = 0.0 WHERE welfare_fee IS NULL")
    conn.commit()
    print(f"Updated {cursor.rowcount} customer records with default welfare_fee")
except Exception as e:
    print(f"Error: {e}")

conn.close()
