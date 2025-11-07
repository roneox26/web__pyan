from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE loans ADD COLUMN application_fee FLOAT DEFAULT 0.0'))
            conn.commit()
        print("Successfully added application_fee column to loans table!")
    except Exception as e:
        print(f"Error: {e}")
