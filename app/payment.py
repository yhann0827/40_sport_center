from flask import json, Flask, jsonify, request, session, Response
from app import app, models, db
import rsa
from datetime import datetime

publicKey, privateKey = rsa.newkeys(512)

@app.route('/payments')
def get_payments():
    payments = models.payment.query.all()
    return jsonify('{"payments":' + str(payments) + '}')

@app.route('/payments', methods=['POST'])
def add_payments():
    card_data = json.loads(request.data.decode("utf-8"))
    print(card_data)
    user_id = int(session['loggedin'])
    print("user_id:")
    card_data['user_id'] = user_id
    print(card_data)
    discount = None
    if 'discount_id' in card_data:
        discount = models.discount.query.filter_by(discount_id=card_data['discount_id']).first()
        print(discount)
    facility = None
    total_price = 0    
    for item in card_data['cart']:
        print(user_id)
        item['user_id'] = user_id
        item['discount_id'] = None
        if discount != None:
            item['discount_id'] = discount.discount_id
        total_price = total_price + item['price']
        if item['type'] == 'Membership':
            now = datetime.now()            
            if item['item'].index('Annual') >= 0:
                year = now.year + 1
                item['date_of_expiry'] = str(year) + now.strftime('-%m-%d')
            else:
                month = str(now.month + 1)
                if len(month) < 2:
                    month = '0' + month
                item['date_of_expiry'] = now.strftime('%y-') + month + now.strftime('-%d')
            item['amount'] = item['price']
            print("item:")
            print(item)
            save_payment(item)
            save_membership(item)
        elif item['type'] == 'Facility':
            facility_id = item['facility_id']
            facility = models.facility.query.filter_by(facility_id=facility_id).first()
            item['facility_id'] = facility_id
            amount = facility.price
            if discount != None:
                amount = amount - (discount.amount * facility.price) / 100
            item['amount'] = amount
            item['price'] = amount
            print("Facility: ")
            print(item)
            payment = save_payment(item)
            print("Payment:")
            print(payment)
            item['payment_id'] = payment.payment_id
            save_booking(item)
        elif item['type'] == 'Class':
            facility_id = item['facility_id']
            facility = models.facility.query.filter_by(facility_id=facility_id).first()
            item['facility_id'] = facility_id
            amount = facility.price
            if discount != None:
                amount = amount - (discount.amount * facility.price) / 100
            item['amount'] = amount
            item['price'] = amount
            print("Class: ")
            print(item)
            payment = save_payment(item)
            print("Payment:")
            print(payment)
            item['payment_id'] = payment.payment_id
            save_booking(item)
    if 'save' in card_data.keys() and card_data['save'] == 'on':
        save_card(card_data)
    return Response("", status=204, mimetype="application/json") #jsonify('{"payment":'+ str(payment_model) + '}')

def is_user_member(user_id):
    memberships = models.membership.query.filter_by(user_id=user_id)
    if memberships == None:
        return False
    for membership in memberships:
        if datetime.now() <= membership.expiry_date:
            return True
    return False

def save_membership(data):
    membership_model = models.membership(data)
    db.session.add(membership_model)
    db.session.commit()
    return membership_model

def save_card(data):
    card_model = models.card(data)
    db.session.add(card_model)
    db.session.commit()
    print(card_model)
    return card_model

def save_payment(data):
    payment_model = models.payment(data)
    db.session.add(payment_model)
    db.session.commit()
    print(payment_model)
    return payment_model

def save_class(data):
    class_model = models.class_table(data)
    db.session.commit()
    print(class_model)
    return class_model

def save_booking(data):
    booking_model = models.sports_booking(data)
    print(booking_model)
    db.session.add(booking_model)
    db.session.commit()
    print(booking_model)
    return booking_model

@app.route('/payments/<payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment_model = models.payment.query.get(int(payment_id))
    payment_data = json.loads(request.data)
    payment_model = models.payment(payment_data)
    db.session.commit()
    return jsonify('{"payment":'+ str(payment_model) + '}')

@app.route('/payments/<payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment_model = models.payment.query.get(int(payment_id))
    db.session.delete(payment_model)
    db.session.commit()
    return 'OK'
