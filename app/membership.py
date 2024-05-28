from flask import json, Flask, jsonify, request
from app import app, models, db

@app.route('/memberships')
def get_members():
    memberships = models.membership.query.all()
    return jsonify('{"memberships":' + str(memberships) + '}')

@app.route('/membership', methods=['POST'])
def add_membership():
    membership_data = json.loads(request.data)
    membership_model = models.membership(membership_data)
    db.session.add(membership_model)
    db.session.commit()
    return jsonify('{"membership":'+ str(membership_model) + '}')

@app.route('/membership/<membership_id>', methods=['PUT'])
def update_membership(membership_id):
    membership_model = models.membership.query.get(int(membership_id))
    membership_data = json.loads(request.data)
    membership_model = models.membership(membership_data)
    db.session.commit()
    return jsonify('{"membership":'+ str(membership_model) + '}')

@app.route('/membership/<membership_id>', methods=['DELETE'])
def delete_membership(membership_id):
    membership_model = models.membership.query.get(int(membership_id))
    db.session.delete(membership_model)
    db.session.commit()
    return 'OK'
