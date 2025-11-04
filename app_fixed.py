from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models.user_model import db, User
import config
from models.staff_model import Staff
from models.loan_model import Loan
from models.saving_model import Saving
from models.customer_model import Customer
from models.collection_model import Collection
from models.loan_collection_model import LoanCollection
from models.saving_collection_model import SavingCollection
from models.cash_balance_model import CashBalance
from models.investment_model import Investment
from models.withdrawal_model import Withdrawal
from models.expense_model import Expense
from models.message_model import Message
from datetime import datetime, timedelta
import csv
import io
import logging

app = Flask(__name__)
app.config.from_object(config)
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
logging.basicConfig(level=logging.DEBUG)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(400)
def bad_request(e):
    logging.error(f"400 Error: {e}")
    logging.error(f"Request data: {request.data}")
    logging.error(f"Request form: {request.form}")
    flash('Invalid request. Please check your input.', 'danger')
    return redirect(request.referrer or url_for('dashboard'))

# ----------- Routes -----------

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        staff_count = User.query.filter_by(role='staff').count()
        total_loans = db.session.query(db.func.sum(Customer.total_loan)).scalar() or 0
        pending_loans = db.session.query(db.func.sum(Customer.remaining_loan)).scalar() or 0
        total_savings = db.session.query(db.func.sum(Customer.savings_balance)).scalar() or 0
        total_customers = Customer.query.count()
        
        cash_balance_record = CashBalance.query.first()
        cash_balance = cash_balance_record.balance if cash_balance_record else 0
        
        period = request.args.get('period', 'all')
        fee_period = request.args.get('fee_period', 'all')
        
        admission_fees = db.session.query(db.func.sum(Customer.admission_fee)).scalar() or 0
        service_charges = db.session.query(db.func.sum(Loan.service_charge)).scalar() or 0
        total_fees = admission_fees + service_charges
        
        return render_template('admin_dashboard.html', name=current_user.name, staff_count=staff_count, total_loans=total_loans, pending_loans=pending_loans, total_savings=total_savings, total_customers=total_customers, cash_balance=cash_balance, period=period, fee_period=fee_period, total_fees=total_fees)
    elif current_user.role == 'staff':
        my_customers = Customer.query.filter_by(staff_id=current_user.id).count()
        total_remaining = db.session.query(db.func.sum(Customer.remaining_loan)).filter_by(staff_id=current_user.id).scalar() or 0
        today = datetime.now().replace(hour=0, minute=0, second=0)
        today_loan_collections = LoanCollection.query.filter_by(staff_id=current_user.id).filter(LoanCollection.collection_date >= today).count()
        today_saving_collections = SavingCollection.query.filter_by(staff_id=current_user.id).filter(SavingCollection.collection_date >= today).count()
        today_collections = today_loan_collections + today_saving_collections
        unread_messages = Message.query.filter_by(staff_id=current_user.id, is_read=False).count()
        return render_template('staff_dashboard.html', name=current_user.name, my_customers=my_customers, total_remaining=total_remaining, today_collections=today_collections, unread_messages=unread_messages)
    else:
        flash('Invalid role!', 'danger')
        return redirect(url_for('logout'))

@app.route('/loan_collection/collect', methods=['POST'])
@login_required
def collect_loan():
    try:
        logging.debug(f"Form data: {request.form}")
        
        customer_id = request.form.get('customer_id')
        amount = request.form.get('amount')
        
        if not customer_id or not amount:
            flash('সব তথ্য পূরণ করুন!', 'danger')
            return redirect(url_for('loan_collection'))
        
        customer_id = int(customer_id)
        amount = float(amount)
        
        logging.debug(f"Customer ID: {customer_id}, Amount: {amount}")
        
        customer = Customer.query.get_or_404(customer_id)
        
        if customer.remaining_loan <= 0:
            flash(f'{customer.name} এর কোনো বকেয়া লোন নেই!', 'warning')
            return redirect(url_for('loan_collection'))
        
        if amount > customer.remaining_loan:
            flash(f'টাকা বাকি লোন থেকে বেশি!', 'danger')
            return redirect(url_for('loan_collection'))
        
        collection = LoanCollection(customer_id=customer_id, amount=amount, staff_id=current_user.id)
        customer.remaining_loan -= amount
        
        cash_balance_record = CashBalance.query.first()
        if not cash_balance_record:
            cash_balance_record = CashBalance(balance=0)
            db.session.add(cash_balance_record)
        cash_balance_record.balance += amount
        
        db.session.add(collection)
        db.session.commit()
        flash(f'সফলভাবে ৳{amount} কালেকশন সম্পন্ন!', 'success')
    except Exception as e:
        logging.error(f"Error in collect_loan: {str(e)}")
        db.session.rollback()
        flash(f'এরর: {str(e)}', 'danger')
    return redirect(url_for('loan_collection'))

@app.route('/saving_collection/collect', methods=['POST'])
@login_required
def collect_saving():
    try:
        customer_id = request.form.get('customer_id')
        amount = request.form.get('amount')
        
        if not customer_id or not amount:
            flash('সব তথ্য পূরণ করুন!', 'danger')
            return redirect(url_for('saving_collection'))
        
        customer_id = int(customer_id)
        amount = float(amount)
        customer = Customer.query.get_or_404(customer_id)
        
        collection = SavingCollection(customer_id=customer_id, amount=amount, staff_id=current_user.id)
        customer.savings_balance += amount
        
        cash_balance_record = CashBalance.query.first()
        if not cash_balance_record:
            cash_balance_record = CashBalance(balance=0)
            db.session.add(cash_balance_record)
        cash_balance_record.balance += amount
        
        db.session.add(collection)
        db.session.commit()
        flash(f'সফলভাবে ৳{amount} সেভিংস জমা!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('এরর হয়েছে!', 'danger')
    return redirect(url_for('saving_collection'))

@app.route('/loan_collection', methods=['GET'])
@login_required
def loan_collection():
    if current_user.role == 'staff':
        customers = Customer.query.filter_by(staff_id=current_user.id).filter(Customer.remaining_loan > 0).all()
    else:
        customers = Customer.query.filter(Customer.remaining_loan > 0).all()
    return render_template('loan_collection.html', customers=customers)

@app.route('/saving_collection', methods=['GET'])
@login_required
def saving_collection():
    if current_user.role == 'staff':
        customers = Customer.query.filter_by(staff_id=current_user.id).all()
    else:
        customers = Customer.query.all()
    return render_template('saving_collection.html', customers=customers)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)