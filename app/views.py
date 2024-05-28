from flask import Flask, jsonify, request, render_template, session, Response, redirect, url_for
from app import app, models

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/users', methods=['GET'])
def users_list():
    # user = session['loggedin']
    # if(user is None):
    #     return Response("Page not found", status=404)
    return render_template('users-list.html')

@app.route('/login', methods=['GET'])
def user_login():
    session['loggedin'] = None
    return render_template('login.html')

@app.route('/sportsbooking', methods=['GET'])
def sports_booking():
    return render_template('new-sportsbooking.html')

@app.route('/classbooking', methods=['GET'])
def class_booking():
    return render_template('new-classbooking.html')

@app.route('/membership', methods=['GET'])
def membership_view():
    return render_template('membership.html')

@app.route('/logout', methods=['GET'])
def logout():
    session['loggedin'] = None
    session['usertype'] = None
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET'])
def checkout():    
    return render_template('new-checkout.html')

@app.route('/account', methods=['GET'])
def account():
    return render_template('customerMyAcc.html')

@app.route('/manager/login', methods=['GET'])
def manager_login():
    return render_template('managerlogin.html')

@app.route('/manager/home', methods=['GET'])
def manager_home():
    return render_template('managerhome.html')

@app.route('/manager/sports', methods=['GET'])
def manager_sports():
    return render_template('managesports.html')

@app.route('/manager/class', methods=['GET'])
def manager_class():
    return render_template('manageclass.html')

@app.route('/manager/staff', methods=['GET'])
def manager_staff():
    return render_template('managestaff.html')

@app.route('/manager/account', methods=['GET'])
def manager_account():
    return render_template('managerMyAcc.html')

@app.route('/manager/logout', methods=['GET'])
def manager_logout():
    session['loggedin'] = None
    session['usertype'] = None
    return redirect(url_for('index'))

@app.route('/booking', methods=['GET'])
def get_my_bookings():
    return render_template('new-booking.html')

@app.route('/cart', methods=['GET'])
def get_cart():
    return render_template('shoppingcart.html')

@app.route('/employee/login', methods=['GET'])
def employee_login():
    return render_template('employeelogin.html')

@app.route('/employee/home', methods=['GET'])
def employee_home():
    return render_template('employeehome.html')

@app.route('/employee/logout', methods=['GET'])
def employee_logout():
    session['loggedin'] = None
    session['usertype'] = None
    return redirect(url_for('index'))

@app.route('/employee/account', methods=['GET'])
def employee_account():
    return render_template('employeeMyAcc.html')

@app.route('/employee/customer', methods=['GET'])
def employee_customer():
    return render_template('employeecustomer.html')

@app.route('/employee/sports', methods=['GET'])
def customer_booking():
    return render_template('employeesports.html')

@app.route('/employee/class', methods=['GET'])
def customer_class_booking():
    return render_template('employeeclassbooking.html')
