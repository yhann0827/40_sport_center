from flask import json, Flask, jsonify, request
from app import app, models, db

@app.route('/managers')
def get_managers():
    managers = models.manager.query.all()
    return jsonify('{"managers":' + str(managers) + '}')

@app.route('/managers', methods=['POST'])
def add_managers():
    manager_data = json.loads(request.data)
    manager_model = models.manager(manager_data)
    db.session.add(manager_model)
    db.session.commit()
    return jsonify('{"manager":'+ str(manager_model) + '}')

@app.route('/managers/<manager_id>', methods=['PUT'])
def update_manager(manager_id):
    manager_model = models.manager.query.get(int(manager_id))
    manager_data = json.loads(request.data)
    manager_model = models.manager(manager_data)
    db.session.commit()
    return jsonify('{"manager":'+ str(manager_model) + '}')

@app.route('/managers/<manager_id>', methods=['DELETE'])
def delete_manager(manager_id):
    manager_model = models.manager.query.get(int(manager_id))
    db.session.delete(manager_model)
    db.session.commit()
    return 'OK'

# link manager to a user
@app.route('/managers/<manager_id>/users/<user_id>', methods=['PUT'])
def assign_user_manager(manager_id, user_id):
    manager_model = models.manager.query.get(int(manager_id))
    manager_model.user_ID = int(user_id)
    user_has_manager = models.user_has_manager(manager_model)
    db.session.add(user_has_manager)
    db.session.commit()
    return jsonify('{"assigned":'+ str(user_has_manager) + '}')

