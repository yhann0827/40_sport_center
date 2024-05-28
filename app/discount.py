from flask import json, Flask, jsonify, request, Response, session
from app import app, models, db
import datetime
from decimal import Decimal
from sqlalchemy import or_

@app.route('/discounts/apply', methods=['GET'])
def apply_discount():
    user_id = session['loggedin']
    item_type = request.args.get("item_type")
    item_qty = int(request.args.get("item_qty"))
    # item_total = Decimal(request.args.get("item_total"))
    if item_type == "Membership":
        return 0
    filters = []
    filters.append(models.membership.user_id==user_id)
    filters.append(models.membership.date_of_expiry > datetime.datetime.now())
    memberships = models.membership.query.filter(or_(*filters)).count()
    is_member = False
    if memberships == 0:
        is_member = False
    applied_to = 'Non Members'
    if is_member:
        applied_to = 'Members'
    discount = models.discount.query.filter_by(applied_to=applied_to).first()
    print(discount)
    if discount.minimum_booking > item_qty:
        return json.loads('{"discount": null}')
    return json.loads('{"discount":'+ str(discount) + '}')

@app.route('/discounts', methods=['POST'])
def add_discounts():
    discount_data = json.loads(request.data)
    discount_model = models.discount(discount_data)
    print(discount_model)
    db.session.add(discount_model)
    db.session.commit()
    return Response("", status=204, mimetype="application/json")

@app.route('/discounts', methods=['PUT'])
def edit_discount():
    discount_data = json.loads(request.data.decode("utf-8"))
    discount_model = models.discount.query.filter_by(discount_id=discount_data['discount_id']).first()
    discount_model.applied_to = discount_data['applied_to']
    discount_model.amount = discount_data['amount']
    discount_model.minimum_booking = discount_data['minimum_booking']
    db.session.commit()
    return Response("", status=204, mimetype="application/json")

@app.route('/discounts/<discount_id>', methods=['DELETE'])
def delete_discount(discount_id):
    discount_model = models.discount.query.filter_by(discount_id=discount_id).first()
    db.session.delete(discount_model)
    db.session.commit()
    return Response("", status=204, mimetype="application/json")
