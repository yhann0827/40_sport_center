from flask import json, Flask, jsonify, request
from app import app, models, db

@app.route('/sessions')
def get_sessions():
    sessions = models.session.query.all()
    return json.loads('{"sessions":' + str(sessions) + '}')

@app.route('/sessions', methods=['POST'])
def add_sessions():
    session_data = json.loads(request.data)
    session_model = models.session(session_data)
    db.session.add(session_model)
    db.session.commit()
    return jsonify('{"session":'+ str(session_model) + '}')

@app.route('/sessions/<session_id>', methods=['PUT'])
def update_session(session_id):
    session_model = models.session.query.get(int(session_id))
    session_data = json.loads(request.data)
    session_model = models.session(session_data)
    db.session.commit()
    return jsonify('{"session":'+ str(session_model) + '}')

@app.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    session_model = models.session.query.get(int(session_id))
    db.session.delete(session_model)
    db.session.commit()
    return 'OK'
