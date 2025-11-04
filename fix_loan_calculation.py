from app import app, db
from models.customer_model import Customer
from models.loan_model import Loan

with app.app_context():
    print("পুরনো লোন ডাটা ঠিক করা হচ্ছে...")
    
    # সব customer এর loan reset করি
    customers = Customer.query.all()
    for customer in customers:
        customer.total_loan = 0
        customer.remaining_loan = 0
    
    # সব loan থেকে নতুন করে হিসাব করি
    loans = Loan.query.all()
    for loan in loans:
        customer = Customer.query.filter_by(staff_id=loan.staff_id).filter(
            db.func.lower(Customer.name) == db.func.lower(loan.customer_name)
        ).first()
        
        if customer:
            # শুধু loan + interest যোগ করি (service_charge এবং welfare_fee বাদ)
            interest_amount = (loan.amount * loan.interest) / 100
            loan_with_interest = loan.amount + interest_amount
            
            customer.total_loan += loan_with_interest
            customer.remaining_loan += loan_with_interest
            
            print(f"Customer: {customer.name}, Loan: ৳{loan.amount}, Interest: ৳{interest_amount}, Total: ৳{loan_with_interest}")
    
    # এখন loan collection গুলো বিয়োগ করি
    from models.loan_collection_model import LoanCollection
    collections = LoanCollection.query.all()
    for collection in collections:
        customer = Customer.query.get(collection.customer_id)
        if customer:
            customer.remaining_loan -= collection.amount
    
    db.session.commit()
    print("\n✅ সফলভাবে সম্পন্ন হয়েছে!")
    print("\nসব customer এর নতুন হিসাব:")
    customers = Customer.query.all()
    for customer in customers:
        if customer.total_loan > 0:
            print(f"{customer.name}: Total Loan = ৳{customer.total_loan:.2f}, Remaining = ৳{customer.remaining_loan:.2f}")
