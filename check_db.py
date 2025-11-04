from app import app, db, User, bcrypt

with app.app_context():
    try:
        users = User.query.all()
        print("\nDatabase connected!")
        print(f"Total users: {len(users)}\n")
        
        for user in users:
            print(f"User: {user.name}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}\n")
        
        if not users:
            print("No users found! Creating default users...")
            
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(name='Admin', email='admin@example.com', password=hashed_pw, role='admin')
            db.session.add(admin)
            
            hashed_pw = bcrypt.generate_password_hash('staff123').decode('utf-8')
            staff = User(name='Staff', email='staff@example.com', password=hashed_pw, role='staff')
            db.session.add(staff)
            
            db.session.commit()
            print("Default users created!")
            print("Admin: admin@example.com / admin123")
            print("Staff: staff@example.com / staff123")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nCreating database tables...")
        db.create_all()
        print("Database tables created!")
