from flask import json, Flask, jsonify, request, Response
from app import app, models, db
import datetime
import decimal

@app.route('/facilities', methods=['GET'])
def get_facilities():
    facilities = db.session.query(models.facility.facility_name).all()
    test = []
    for facility in facilities:
        s = '{ "facility_name": "' + facility.facility_name + '" }'
        if not test.__contains__(s):
            test.append(s)

    return json.loads('{"facilities":' + json.dumps(test) + '}')

@app.route('/facilities/list', methods=['GET'])
def get_facilities_list():
    db.session.expire_all()
    facilities = models.sports_facility.query.all()
    activities = models.sports_activity.query.all()
    classes = models.sports_activity_class.query.all()
    discounts = models.discount.query.all()
    print(discounts)
    return json.loads('{"facilities":' + str(facilities) + ', "activities":'+ str(activities) + ', "classes":'+ str(classes)+ ', "discounts":'+ str(discounts) + '}')

@app.route('/facilities', methods=['POST'])
def add_facilities():
    facility_data = json.loads(request.data)
    facility_model = models.facility(facility_data)
    db.session.add(facility_model)
    db.session.commit()
    return Response("", status=204, mimetype="application/json")

@app.route('/facilities', methods=['PUT'])
def edit_facility():
    facility_data = json.loads(request.data.decode("utf-8"))
    facility_model = models.facility.query.filter_by(facility_id=facility_data['facility_id']).first()
    facility_model.start_time = datetime.datetime.strptime(facility_data['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    facility_model.end_time = datetime.datetime.strptime(facility_data['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    facility_model.facility_name = facility_data['facility_name']
    facility_model.price = facility_data['price']
    facility_model.description = facility_data['description']
    db.session.commit()
    return Response("", status=204, mimetype="application/json")

@app.route('/classes/list', methods=['GET'])
def get_classes():
    classes = models.class_table.query.all()
    facilities = models.facility.query.all()
    return json.loads('{"classes":' + str(classes) + ',"facilities":' + str(facilities) + '}')

@app.route('/classes', methods=['GET'])
def get_class_list():
    classes = models.class_table.query.all()
    return json.loads('{"classes":' + str(classes) + '}')

@app.route('/classes', methods=['PUT'])
def edit_classes():
    class_data  = json.loads(request.data.decode("utf-8"))
    class_model = models.class_table.query.filter_by(class_id=class_data['class_id']).first()
    if class_model == None:
        return Response("Class does not exist", status=400, mimetype="application/json")
    class_model.class_name = class_data['class_name']
    class_model.class_capacity = int(class_data['class_capacity'])
    class_model.price = class_data['price']
    db.session.commit()
    return Response("Class saved", status=204, mimetype="application/json")

@app.route('/facilities/<facility_id>', methods=['DELETE'])
def delete_facility(facility_id):
    facility_model = models.facility.query.filter_by(facility_id=facility_id).first()
    db.session.delete(facility_model)
    db.session.commit()
    return Response("", status=204, mimetype="application/json")
