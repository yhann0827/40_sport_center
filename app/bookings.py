from flask import json, Flask, jsonify, request, Response, session
from app import app, models, db
from sqlalchemy import or_, and_
import datetime

@app.route('/bookings', methods=['GET'])
def get_bookings():
    user_id = session['loggedin']
    bookings = models.sports_booking.query.filter_by(user_id=user_id).all()
    booking_data = []
    for b in bookings:
        facility = models.sports_facility.query.filter_by(id=b.facility_id).first()
        activity = models.sports_activity.query.filter_by(id=b.activity_id).first()
        if b.class_id != None:
            booking_class = models.sports_activity_class.query.filter_by(id=b.class_id).first()
            book.class_name = booking_class.class_name
        book = models.booking_d()
        book.booking_id = b.id
        book.facility = facility.facility_name
        book.activity = activity.activity_name
        book.start_time = b.start_time
        book.end_time = b.end_time
        book.amount = b.price
        booking_data.append(book)
        print(booking_data)
    return json.loads('{"bookings":' + str(booking_data) + '}')

@app.route('/classes/check')
def check_class_availibility():
    print(request.data)
    request_data = json.loads(request.data.decode("utf-8"))
    print(request_data)
    classes = models.class_table.query.filter_by(class_name=request_data['class_name'])
    class_t = None
    return

@app.route('/bookings/class/check', methods=['POST'])
def check_class_availability():
    print(request.data)
    request_data = json.loads(request.data.decode("utf-8"))
    print(request_data)
    classes = models.class_table.query.filter_by(class_name=request_data['class_name']).all()
    class_t = None
    for c in classes:
        facility = models.facility.query.filter_by(facility_id=c.facility_id).first()
        print(c.facility_id)
        print(facility)
        print(facility.start_time, datetime.datetime.strptime(request_data['check_start_time'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        if facility.start_time >= datetime.datetime.strptime(request_data['check_start_time'], '%Y-%m-%dT%H:%M:%S.%fZ') and \
            facility.end_time <= datetime.datetime.strptime(request_data['check_end_time'], '%Y-%m-%dT%H:%M:%S.%fZ') :
            class_t = c

    if(class_t == None):
        return Response("Class not found", status=404, mimetype='application/json')

    if(class_t.class_capacity > 0):
        return Response('{"class":'+ str(class_t)+ '}', status=200, mimetype="application/json")
    else:
        return request_data, 400

@app.route('/sports-bookings/check', methods=['POST'])
def check_facility_availability():
    request_data = json.loads(request.data.decode("utf-8"))
    print(request_data)
    facility = models.sports_facility.query.filter_by(id=request_data['facility_id']).first()
    activity = models.sports_activity.query.filter_by(id=request_data['activity_id']).first()
    print(facility)
    print(activity)
    filters = []
    filters.append(models.sports_booking.id==request_data['facility_id'])
    filters.append(models.sports_booking.id==request_data['activity_id'])
    if 'class_id' in request_data:
        print("Class ID:")
        print(request_data['class_id'])
        filters.append(models.sports_booking.class_id==request_data['class_id'])
    filters.append(models.sports_booking.start_time==datetime.datetime.strptime(request_data['check_start_time'], '%Y-%m-%dT%H:%M:%S.%fZ'))
    filters.append(models.sports_booking.end_time==datetime.datetime.strptime(request_data['check_end_time'], '%Y-%m-%dT%H:%M:%S.%fZ'))
    print(*filters)
    bookings = models.sports_booking.query.filter(and_(*filters)).all()
    print("Bookings: "+str(len(bookings)))
    if len(bookings) == 0:
        return Response('', status=204, mimetype="application/json")
    else:
        if facility.capacity < (len(bookings) + activity.unit):
            return Response('', status=204, mimetype="application/json")
    return Response('', status=404, mimetype="application/json")

@app.route('/bookings/check', methods=['POST'])
def check_availability():
    print(request.data)
    request_data = json.loads(request.data.decode("utf-8"))
    print(request_data)
    facilities = models.facility.query.filter_by(facility_name=request_data['facility_name']).all()
    facility = None
    for f in facilities:
        print(f.start_time, datetime.datetime.strptime(request_data['check_start_time'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        if f.start_time >= datetime.datetime.strptime(request_data['check_start_time'], '%Y-%m-%dT%H:%M:%S.%fZ') and \
            f.end_time <= datetime.datetime.strptime(request_data['check_end_time'], '%Y-%m-%dT%H:%M:%S.%fZ') :
            facility = f

    if(facility == None):
        return Response("Facility not found", status=404, mimetype='application/json')

    no_of_bookings = models.booking.query.filter_by(facility_id=facility.facility_id).count()
    if no_of_bookings > 0:
        return request_data, 400
    else:
        print(facility.facility_id)
        session['facility'] = facility.facility_id
        return Response('{"facility":'+ str(facility.facility_id)+ '}', status=200, mimetype="application/json")

# @app.route('/bookings', methods=['POST'])
# def add_booking():
#     try:
#         request_data = json.loads(request.data)
#         booking = models.booking(request_data)
#         db.session.add(booking)
#         db.session.commit
#         return json.loads(str(booking)), 204
#     except:
#          return Response("Server error", status=500, mimetype='application/json')

