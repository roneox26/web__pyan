import os
import time

db_path = 'instance/loan.db'

print("Waiting for database to be released...")
time.sleep(2)

if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✓ Database deleted: {db_path}")
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nPlease:")
        print("1. Stop your Flask app (Ctrl+C)")
        print("2. Run this script again")
else:
    print(f"Database not found: {db_path}")

print("\nNow run your app.py to create new database with updated schema.")
