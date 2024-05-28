from flask import json, Flask, jsonify, request, session, Response
from flask_cors import cross_origin
from app import app, models, db
from sqlalchemy import or_
import datetime as dt
import hashlib

hash_key = " xXcCvVbBnNmM"

@app.route('/users/customerlist', methods=['GET'])
def get_customers():
    db.session.expire_all()
    Users = models.user.query.filter_by(user_type=models.UserType.Customer).all()
    return json.loads('{"users":' + str(Users) + '}')

@app.route('/users/list', methods=['GET'])
def get_users():
    db.session.expire_all()
    Users = models.user.query.all()
    return json.loads('{"users":' + str(Users) + '}')

@app.route('/users/my', methods=['GET'])
def get_user_detail():
    db.session.expire_all()
    user_id = session['loggedin']
    print("User ID:")
    print(user_id)
    me = models.user.query.filter_by(user_id=user_id).first()
    print("User:")
    print(me)
    membership = models.membership.query.filter_by(user_id=user_id).first()
    print("Membership:")
    print(membership)
    detail = ""
    if(membership != None):
        detail = ', "membership":' + str(membership)
    return json.loads('{"user":' + str(me) + detail + '}')

@app.route('/users', methods=['POST'])
def create_user():
    user_data = json.loads(request.data.decode("utf-8"))
    print(user_data)
    if 'user_type' not in user_data:
        user_data['user_type'] = "Customer" 
    print(user_data)
    user = add_users(user_data)
    if (user == -1):
        return Response("User already exists", status=400, mimetype="application/json")
    if(user == None):
        return Response("Server error", status=400, mimetype="application/json")
    return Response("", status=204, mimetype="application/json")

def add_users(user_data):
    try:
        print(user_data['email'])
        existing = models.user.query.filter_by(email=user_data['email']).count()
        print("Found: " + str(existing))
        if (existing != 0):
            return -1
        user_model = models.user(user_data)
        user_model.password = hash(user_model.password)
        db.session.add(user_model)
        db.session.commit()
        return user_model
    except:
         return None

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_model = models.user.query.get(int(user_id))
        if user_model is None:
            return Response("Record not found", status=400, mimetype='application/json')
        user_data = json.loads(request.data)
        user_model.first_name=user_data['first_name']
        user_model.last_name=user_data['last_name']
        user_model.username=user_data['username']
        user_model.password =  user_data['password']
        user_model.email=user_data['email']
        user_model.date_of_birth=dt.datetime.strptime(user_data['date_of_birth'], '%Y-%m-%dT%H:%M:%S')
        user_model.user_type=models.UserType[user_data['user_type']]
        db.session.commit()
        return json.loads('{"user":'+ str(user_model) + '}')
    except:
        return Response("Server error", status=500, mimetype='application/json')

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_model = models.user.query.get(int(user_id))
        if user_model is None:
            return Response("Record not found", status=400, mimetype='application/json')
        db.session.delete(user_model)
        db.session.commit()
        return Response("Record deleted", status=200, mimetype='application/json')
    except:
            return Response("Server error", status=500, mimetype='application/json')

def hash(password):
    h = hashlib.sha256()
    h.update(password.encode('utf-8'))
    h.digest()
    return str(h.hexdigest())

@app.route('/users/login', methods=['POST'])
def login():
    login_data = json.loads(request.data.decode("utf-8"))
    email = login_data['email']
    print(email)
    password = hash(login_data['password'])
    print(password)
    filters = []
    filters.append(models.user.email==email)
    filters.append(models.user.password==password)
    found = models.user.query.filter(or_(*filters)).first()
    print("Found: " + str(found))
    session['loggedin'] = str(found.user_id)
    session['usertype'] = str(found.user_type)
    print("User ID: " + session['loggedin'])
    print("User Type: " + session['usertype'])
    if found is None:
        return Response("User not found", status=404, mimetype='application/json')
    else:
        return Response("Login successful", status=204, mimetype='application/json')
