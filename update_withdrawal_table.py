from app import app, db
from models.withdrawal_model import Withdrawal

with app.app_context():
    # Add new columns to withdrawals table
    with db.engine.connect() as conn:
        try:
            # Check if columns exist, if not add them
            conn.execute(db.text("ALTER TABLE withdrawals ADD COLUMN customer_id INTEGER"))
            print("Added customer_id column")
        except Exception as e:
            print(f"customer_id column might already exist: {e}")
        
        try:
            conn.execute(db.text("ALTER TABLE withdrawals ADD COLUMN withdrawal_type VARCHAR(20) DEFAULT 'investment'"))
            print("Added withdrawal_type column")
        except Exception as e:
            print(f"withdrawal_type column might already exist: {e}")
        
        try:
            # Make investor_name nullable
            conn.execute(db.text("ALTER TABLE withdrawals MODIFY COLUMN investor_name VARCHAR(100) NULL"))
            print("Modified investor_name to be nullable")
        except Exception as e:
            print(f"Could not modify investor_name: {e}")
        
        conn.commit()
    
    print("Database updated successfully!")
