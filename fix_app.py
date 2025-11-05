from app import app, db
from models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    try:
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if admin exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(name='Admin', email='admin@example.com', password=hashed_pw, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
        else:
            print("Admin user already exists!")
        
        # Check if staff exists
        staff = User.query.filter_by(email='staff@example.com').first()
        if not staff:
            hashed_pw = bcrypt.generate_password_hash('staff123').decode('utf-8')
            staff = User(name='Staff', email='staff@example.com', password=hashed_pw, role='staff')
            db.session.add(staff)
            db.session.commit()
            print("Staff user created!")
        else:
            print("Staff user already exists!")
            
        print("\nSetup completed successfully!")
        print("You can now run: python app.py")
        
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
