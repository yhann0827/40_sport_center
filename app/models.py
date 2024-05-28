from app import db
import enum
import datetime as dt
from decimal import Decimal

class UserType(enum.Enum):
    Customer = "Customer"
    Employee = "Employee"
    Manager = "Manager"   

class class_table(db.Model):
    def __init__(self, class_table_data):
        self.facility_id = class_table_data['facility_id']
        self.class_name = class_table_data['class_name']
        self.class_capacity = class_table_data['class_capacity']
        self.price = class_table_data['price']
    def __repr__(self):
        return '{ "class_id": ' + str(self.class_id) + ', "facility_id": ' + str(self.facility_id) + ', "class_name":"'+ self.class_name + \
        '","class_capacity":'+ str(self.class_capacity) + ',"price":' + str(self.price) + '}'
    class_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.facility_id'))
    class_name = db.Column(db.String(50), nullable=False)
    class_capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class discount(db.Model):
    def __init__(self, discount_data):
        self.minimum_booking = discount_data['minimum_booking']
        self.amount = discount_data['amount']
        self.applied_to = discount_data['applied_to']
    def __repr__(self):
        return '{ "discount_id": ' + str(self.discount_id) + ', "amount":' + str(self.amount) + ', "minimum_booking":'+ str(self.minimum_booking) + \
        ',"applied_to":"' + self.applied_to + '"}'
    discount_id = db.Column(db.Integer, primary_key=True)
    applied_to = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    minimum_booking = db.Column(db.Integer, nullable=False)

class user(db.Model):
    def __init__(self, user_data):
        self.first_name=user_data['first_name']
        self.last_name=user_data['last_name']
        self.password =  user_data['password']
        self.email=user_data['email']
        self.date_of_birth=dt.datetime.strptime(user_data['date_of_birth'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.user_type = UserType(user_data['user_type'])
    def __repr__(self):
        return '{ "user_id": ' + str(self.user_id) + ', "last_name":"' + self.last_name + '", "first_name":"'+ self.first_name + \
        '","email":"'+ self.email + '","pass":"' + self.password + '","date_of_birth":"' + \
        self.date_of_birth.strftime('%Y-%m-%dT%H:%M:%S') + '","user_type":"' + self.user_type.value + '"}'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)

class card(db.Model):
    def __init__(self, card_data):
        self.user_id = card_data['user_id']
        self.card_number = card_data['card_number']
        self.expiry_date = dt.datetime.strptime(card_data['expiry_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.billing_address = card_data['billing_address']
        self.country = card_data['country']
        self.cvc = card_data['cvc']
        self.city = card_data['city']
        self.state = card_data['state']
        self.postal = card_data['postal']
    def __repr__(self):
        return '{"card_id":' + str(self.card_id) + ',' + \
        '"user_id":' + str(self.user_id) + ',' + \
        '"card_number":"' + self.card_number + '",' + \
        '"expiry_date":"' + str(self.expiry_date) + '",' + \
        '"billing_address":"' + self.billing_address + '",' + \
        '"country":"' + self.country + '",' + \
        '"cvc":"' + self.cvc + '",' + \
        '"city":"' + self.city + '",' + \
        '"state":"' + self.state + '",' + \
        '"postal":"' + self.postal + '"}'
    card_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    card_number = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    billing_address = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    cvc = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal = db.Column(db.String(20), nullable=False)


class payment(db.Model):
    def __init__(self, payment_data):
        self.user_id = payment_data['user_id']
        self.discount_id = payment_data['discount_id']
        self.amount = payment_data['amount']
    def __repr__(self):
        return '{ "payment_id": ' + str(self.payment_id) + \
        ',"user_id": ' + str(self.user_id) + \
        ',"amount":'+ str(self.amount) + '"}'
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.discount_id'))
    amount = db.Column(db.Numeric(10,2), nullable=False)

class membership(db.Model):
    def __init__(self, membership_data):
        self.user_id = membership_data['user_id']
        self.date_of_expiry = dt.datetime.strptime(membership_data['date_of_expiry'], '%Y-%m-%d')
    def __repr__(self):
        return '{ "membership_id": ' + str(self.membership_id) + \
        ',"user_id": ' + str(self.user_id) + \
        ',"date_of_expiry": "' + self.date_of_expiry.strftime('%Y-%m-%dT%H:%M:%S') + '"}'
    membership_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) 
    date_of_expiry = db.Column(db.DateTime, nullable=False)

class facility(db.Model):
    def __init__(self, facility_data):
        self.start_time = dt.datetime.strptime(facility_data['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.end_time = dt.datetime.strptime(facility_data['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.facility_name = facility_data['facility_name']
        self.price = facility_data['price']
        self.description = facility_data['description']
    def __repr__(self):
        return '{ "facility_id": ' + str(self.facility_id) + \
        ',"start_time": "' + self.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ') +  \
        '","end_time": "' + self.end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ') +  \
        '","facility_name": "' + self.facility_name +  \
        '", "price":'+ str(self.price) + \
        ', "description":"'+ self.description + \
        '"}'
    def starttime(self):
        return self.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    def endtime(self):
        return self.end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    facility_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    facility_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.String(100), nullable=False)

class booking(db.Model):
    def __init__(self, booking_data):
        self.user_id = booking_data['user_id']
        self.facility_id = booking_data['facility_id']
        self.payment_id = booking_data['payment_id']
        self.total_price = booking_data['total_price']
    def __repr__(self):
        return '{ "booking_id": ' + str(self.booking_id) + \
        ',"user_id":'+ str(self.user_id) + \
        ',"facility_id": ' + str(self.facility_id) + \
        ',"payment_id":'+ str(self.payment_id) + \
        ',"total_price":"'+ str(self.total_price) + '}'
    booking_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.facility_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    total_price = db.Column(db.Numeric(10,2), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.payment_id'))

class booking_d():
    def __init__(self):
        self.booking_id = 0
        self.facility = ""
        self.activity = ""
        self.class_name = ""
        self.start_time = dt.datetime.now()
        self.end_time = dt.datetime.now()
        self.amount = 0.0
    def __repr__(self):
        return '{"booking_id":' + str(self.booking_id) + ',' + \
            '"facility":"' + self.facility + '",' + \
            '"activity":"' + self.activity + '",' + \
            '"class_name":"' + self.class_name + '",' + \
            '"start_time":"' + self.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ') + '",' + \
            '"end_time":"' + self.end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ') + \
            '","amount":'+ str(self.amount) + '}'

class sports_facility(db.Model):
    def __init__(self, data):
        self.facility_name = data['facility_name']
        self.capacity = data['capacity']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
    def __repr__(self):
        return '{"id":'+str(self.id)+',"facility_name":"'+self.facility_name+'","capacity":'+str(self.capacity)+', "start_time":"'+self.start_time+'", "end_time":"'+ \
            self.end_time+'", "is_classes":'+ str(self.is_classes).lower() +'}'
    id = db.Column(db.Integer, primary_key=True)
    facility_name = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    is_classes = db.Column(db.Boolean, nullable=False)

class sports_activity(db.Model):
    def __init__(self, data):
        self.facility_id = data['facility_id']
        self.activity_name = data['activity_name']
        self.is_team = data['is_team']
        self.duration = data['duration']
        self.unit = data['unit']
        self.price = data['price']
    def __repr__(self):
        return '{' +\
            '"id":'+str(self.id)+', "facility_id":'+str(self.facility_id)+',"activity_name":"'+self.activity_name+'",' +\
                '"is_team":'+str(self.is_team).lower()+',"duration":'+str(self.duration)+', "unit":'+str(self.unit)+',"price":'+str(self.price)+'}'
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('sports_facility.id'))
    activity_name = db.Column(db.String(200), nullable=False)
    is_team = db.Column(db.Boolean, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

class sports_activity_class(db.Model):
    def __init__(self, data):
        self.sports_activity_id = data['sports_activity_id']
        self.day_of_week = data['day_of_week']
        self.class_name = data['class_name']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
    def __repr__(self):
        return '{"id":'+str(self.id)+',"sports_activity_id":'+str(self.sports_activity_id)+',"class_name":"'+self.class_name+'",'+\
            '"day_of_week":'+str(self.day_of_week)+',"start_time":"'+self.start_time+'","end_time":"'+self.end_time+'"}'
    id = db.Column(db.Integer, primary_key=True)
    sports_activity_id = db.Column(db.Integer, db.ForeignKey('sports_activity.id'))
    class_name = db.Column(db.String(100), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)

class sports_booking(db.Model):
    def __init__(self, data):
        self.user_id = data['user_id']
        self.facility_id = data['facility_id']
        self.activity_id = data['activity_id']
        if 'class_id' in data:
            self.class_id = data['class_id']
        self.price = data['price']
        self.payment_id = data['payment_id']
        self.start_time = dt.datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.end_time = dt.datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    def __repr__(self):
        return '{"id":'+str(self.id)+', "facility_id":'+str(self.facility_id)+',"activity_id":'+str(self.activity_id)+',' + \
            '"start_time":"'+self.start_time.strftime('%Y-%m-%dT%H:%M:%S')+'",'+\
            '"end_time":"'+self.end_time.strftime('%Y-%m-%dT%H:%M:%S')+'"}'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    facility_id = db.Column(db.Integer, db.ForeignKey('sports_facility.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('sports_activity.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('sports_activity_class.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.payment_id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
