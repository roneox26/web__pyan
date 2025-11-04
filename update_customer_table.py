from app import app, db
from models.customer_model import Customer

with app.app_context():
    db.create_all()
    print("Database tables created/updated successfully!")
