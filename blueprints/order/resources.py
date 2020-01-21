from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app, admin_required
from .model import Order
from blueprints.user.model import Users
from blueprints.order_details.model import Order_Details
from datetime import datetime
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
import hashlib

bp_order = Blueprint('Order', __name__)
api = Api(bp_order)

class OrderResource(Resource):
    @jwt_required
    def get(self, id):
        claims = get_jwt_claims()
        qry = Order.query.get(id)
        if qry is None:
            return {'message': 'Order is not found'}, 404, {'Content-Type': 'application/json'}
        if qry.user_id is not claims['id']:
            return {'message': 'You are not authorized'}, 403, {'Content-Type': 'application/json'}
        order = marshal(qry, Order.Order_fields)
        qry2 = Order_Details.query.filter_by(order_id=qry.id)
        detail = []
        for row in qry2.all():
            detail.append(marshal(row, Order_Details.Order_Details_fields))
        order['detail']=detail
        return order, 200, {'Content-Type': 'application/json'}


    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('shipping', location='json')
        parse.add_argument('payment', location='json')
        parse.add_argument('tot_price', location='json')
        parse.add_argument('discount', location='json')
        parse.add_argument('shipping_price', location='json')
        parse.add_argument('tot_qty', location='json')
        parse.add_argument('finished', location='json')
        args = parse.parse_args()

        qry = Users.query.get(claims['id'])
        user = marshal (qry, Users.Users_fields)

        newOrder = Order(user['id'], args['shipping'], args['payment'], args['tot_price'], args['discount'], args['shipping_price'], args['tot_qty'], args['finished'])
        db.session.add(newOrder)
        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return {'message' : "Adding Order successful!"},200,{'Content-Type': 'application/json'}

    @jwt_required
    def put(self, id):
        claims = get_jwt_claims()
        qry = Order.query.get(id)
        if qry is None:
            return {'message': 'Order is not found'}, 404, {'Content-Type': 'application/json'}
        if qry.user_id is not claims['id']:
            return {'message': 'You are not authorized'}, 403, {'Content-Type': 'application/json'}

        parse = reqparse.RequestParser()
        parse.add_argument('shipping', location='json')
        parse.add_argument('payment', location='json')
        parse.add_argument('tot_price', location='json')
        parse.add_argument('discount', location='json')
        parse.add_argument('shipping_price', location='json')
        parse.add_argument('tot_qty', location='json')
        parse.add_argument('finished', location='json')
        args = parse.parse_args()

        qry.shipping = args['shipping'] if args['shipping'] is not None else qry.shipping
        qry.payment = args['payment'] if args['payment'] is not None else qry.payment
        qry.tot_price = args['tot_price'] if args['tot_price'] is not None else qry.tot_price
        qry.discount = args['discount'] if args['discount'] is not None else qry.discount
        qry.shipping_price = args['shipping_price'] if args['shipping_price'] is not None else qry.shipping_price
        qry.tot_qty = args['tot_qty'] if args['tot_qty'] is not None else qry.tot_qty
        qry.finished = args['finished'] if args['finished'] is not None else qry.finished

        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, Order.Order_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        qry = Order.query.get(id)
        if qry is None:
            return {'message': 'Order is not found'}, 404, {'Content-Type': 'application/json'}
        if qry.user_id is not claims['id']:
            return {'message': 'You are not authorized'}, 403, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()
        Order = marshal(qry, Order.Order_fields)
        return {'Order': Order, 'message': 'Order deleted!'}, 200, {'Content-Type': 'application/json'}

    def options(self):
        return {'status': 'OK'}, 200

class OrderList(Resource):
    @jwt_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('username', location='args')
        parser.add_argument('orderby', location='args', help='Invalid orderby value', choices=('user_id', 'id', 'created_at'))
        parser.add_argument('sort', location='args', help='Invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        user = Users.query.filter(Users.username.like("%"+args['username']+"%")).first() if args['username'] is not None else None
        qry = Order.query

        qry = qry.filter_by(user_id=user.id) if user is not None else qry

        if args['orderby'] is not None:
            orderby = 'Order.'+str(args['orderby'])
            if args['sort'] is not None and args['sort']=='desc':
                orderby = str(args['sort'])+'('+'Order.'+str(args['orderby'])+')'
            qry = qry.order_by(eval(orderby))
        
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            qry2 = Order_Details.query.filter_by(order_id=row.id)
            payment = []
            for detail in qry2.all():
                payment.append(detail, Order_Details.Order_Details_fields)
            
            order = marshal(row, Order.Order_fields)
            order['order_details'] = payment
            qry3 = Users.query.get(row.user_id)
            order['name'] = "Order by{name} on {created_at} ({finished})".format(name=qry3.name, created_at=row.created_at, finished=row.finished)
            row.append(order)
        if not rows:
            return {'message': 'No order have been made'}, 404, {'Content-Type':'application/json'}
        return rows, 200
    
    def options(self):
        return {'status': 'OK'}, 200

api.add_resource(OrderResource, '','/<id>')
api.add_resource(OrderList, '/list')
