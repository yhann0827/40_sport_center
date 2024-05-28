from flask import json, Flask, jsonify, request, session, Response
from flask_sqlalchemy import SQLAlchemy, inspect
from app import app, models, db, user

@app.route('/customers')
def get_customers():
    Customers = models.customer.query.all()
    return jsonify('{"customers":' + str(Customers) + '}')

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        user_data = json.loads(request.data.decode("utf-8"))
        inspector = inspect(db.engine)
        table_exists = inspector.has_table("user")
        if table_exists:
            existing = models.user.query.filter_by(username=user_data['username']).count()
            if (existing > 0):
                return Response("Username already taken", status=400, mimetype='application/json')
        user_model = models.user(user_data)
        user_model.user_type = models.UserType.CUSTOMER
        user_model.password = user.hash(user_model.password)
        db.session.add(user_model)
        db.session.commit()
        customer_model = models.customer(user_model.user_id)
        db.session.add(customer_model)
        db.session.commit()
        return Response("", status=204, mimetype='application/json')
    except:
         return Response("Server error", status=500, mimetype='application/json')

@app.route('/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer_model = models.customer.query.get(int(customer_id))
    customer_data = json.loads(request.data)
    customer_model = models.customer(customer_data)
    db.session.commit()
    return jsonify('{"customer":'+ str(customer_model) + '}')

@app.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer_model = models.customer.query.get(int(customer_id))
    db.session.delete(customer_model)
    db.session.commit()
    return 'OK'

# link customer to a user
@app.route('/customers/assign/<customer_id>/users/<user_id>', methods=['PUT'])
def assign_user_customer(customer_id, user_id):
    customer_model = models.customer.query.get(int(customer_id))
    customer_model.user_ID = int(user_id)
    user_has_customer = models.user_has_customer(customer_model)
    db.session.add(user_has_customer)
    db.session.commit()
    return jsonify('{"assigned":'+ str(user_has_customer) + '}')

