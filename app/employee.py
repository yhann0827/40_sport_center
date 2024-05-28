from flask import json, Flask, jsonify, request
from app import app, models, db

@app.route('/employees')
def get_employees():
    employees = models.employee.query.all()
    return jsonify('{"employees":' + str(employees) + '}')

@app.route('/employees', methods=['POST'])
def add_employees():
    employee_data = json.loads(request.data)
    employee_model = models.employee(employee_data)
    db.session.add(employee_model)
    db.session.commit()
    return jsonify('{"employee":'+ str(employee_model) + '}')

@app.route('/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee_model = models.employee.query.get(int(employee_id))
    employee_data = json.loads(request.data)
    employee_model = models.employee(employee_data)
    db.session.commit()
    return jsonify('{"employee":'+ str(employee_model) + '}')

@app.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee_model = models.employee.query.get(int(employee_id))
    db.session.delete(employee_model)
    db.session.commit()
    return 'OK'

# link employee to a user
@app.route('/employees/<employee_id>/users/<user_id>', methods=['PUT'])
def assign_user_employee(employee_id, user_id):
    employee_model = models.employee.query.get(int(employee_id))
    employee_model.user_ID = int(user_id)
    user_has_employee = models.user_has_employee(employee_model)
    db.session.add(user_has_employee)
    db.session.commit()
    return jsonify('{"assigned":'+ str(user_has_employee) + '}')

