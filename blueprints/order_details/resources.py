from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app, admin_required
from .model import Order_Details
from blueprints.user.model import Users
from datetime import datetime
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
import hashlib

bp_order_details = Blueprint('Order_Details', __name__)
api = Api(bp_order_details)

class OrderDetailResource(Resource):
    @jwt_required
    def get(self, id):
        qry = Order_Details.query.get(id)
        if qry is None:
            return {'message': 'Order Details is not found'}, 204, {'Content-Type': 'application/json'}
        return marshal(qry, Order_Details.Order_Details_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('order_id', location='json', required=True)
        parse.add_argument('product_id', location='json', required=True)
        parse.add_argument('qty', location='json', required=True)
        parse.add_argument('tot_price', location='json', required=True)
        args = parse.parse_args()

        newOrderDetails = Order_Details(args['order_id'], args['product_id'], args['qty'], args['tot_price'])
        db.session.add(newOrderDetails)
        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return {'message' : "Adding Order_Details successful!"},200,{'Content-Type': 'application/json'}

    @jwt_required
    def put(self, id):
        qry = Order_Details.query.get(id)
        if qry is None:
            return {'message': 'Order Details is not found'}, 404, {'Content-Type': 'application/json'}

        parse = reqparse.RequestParser()
        parse.add_argument('order_id', location='json')
        parse.add_argument('product_id', location='json')
        parse.add_argument('qty', location='json')
        parse.add_argument('tot_price', location='json')
        args = parse.parse_args()

        qry.order_id = args['order_id'] if args['order_id'] is not None else qry.order_id
        qry.product_id = args['product_id'] if args['product_id'] is not None else qry.product_id
        qry.qty = args['qty'] if args['qty'] is not None else qry.qty
        qry.tot_price = args['tot_price'] if args['tot_price'] is not None else qry.tot_price

        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, Order_Details.Order_Details_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, id):
        qry = Order_Details.query.get(id)
        if qry is None:
            return {'message': 'Order Details is not found'}, 404, {'Content-Type': 'application/json'}
        db.session.delete(qry)
        db.session.commit()
        Order_Details = marshal(qry, Order_Details.Order_Details_fields)
        return {'Order_Details': Order_Details, 'message': 'Order_Details deleted!'}, 200, {'Content-Type': 'application/json'}

    def options(self):
        return {'status': 'OK'}, 200

class OrderDetailsList(Resource):
    @jwt_required
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('order_id', location='json', required=True)
        args = parse.parse_args()

        qry = Order_Details.qry.filter_by(order_id = args['order_id'])

        rows = []
        for row in qry.all():
            rows.append(marshal(row, Order_Details.Order_Details_fields))
        if not rows:
            return {'message': 'No order have been made'}, 404, {'Content-type': 'application/json'}
        return rows, 200, {'Content-Type': 'application/json'}

    def options(self):
        return {'status': 'OK'}, 200

api.add_resource(OrderDetailResource, '', '/<id>')