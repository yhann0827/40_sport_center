from flask import json, Flask, jsonify, request, Response
from app import app, models, db
import datetime
import decimal

@app.route('/sports-facilities', methods=['GET'])
def get_sports_facilities():
    sports_facilities = models.sports_facility.query.all()
    sprots_activities = models.sports_activity.query.all()
    sports_activity_classes = models.sports_activity_class.query.all()
    resp = '{"facilities":'+str(sports_facilities)+', "activities":'+str(sprots_activities)+', "classes":'+ str(sports_activity_classes) +'}'
    return Response(resp, status=200, mimetype="application/json")
