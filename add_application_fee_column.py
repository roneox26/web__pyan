from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Add application_fee column to customers table
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE customers ADD COLUMN application_fee FLOAT DEFAULT 0.0'))
            conn.commit()
        print("Successfully added application_fee column to customers table!")
    except Exception as e:
        print(f"Error: {e}")
        print("Column might already exist or there's another issue.")
