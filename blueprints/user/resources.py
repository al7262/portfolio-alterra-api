from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app, admin_required
from .model import Users
from blueprints.user_details.model import User_Details
from blueprints.order.model import Order
from datetime import datetime
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
import hashlib

bp_user = Blueprint('User', __name__)
api = Api(bp_user)

class UserResource(Resource):
    policy = PasswordPolicy.from_names(
        length = 6,
        uppercase = 1,
        numbers = 1
    )

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', required=True)
        parse.add_argument('email', location='json', required=True)
        parse.add_argument('password', location='json', required=True)
        args = parse.parse_args()

        validation = self.policy.test(args['password'])
        if validation:
            errorList = []
            for item in validation:
                split = str(item).split('(')
                error, num = split[0], split[1][0]
                errorList.append("{err}(minimum {num})".format(err=error, num=num))
            message = "Please check your password: " + ', '.join(x for x in errorList)
            return {'message': message}, 422, {'Content-Type': 'application/json'}
        encrypted = hashlib.md5(args['password'].encode()).hexdigest()

        newUser = Users(username=args['username'], email=args['email'], password=encrypted)
        db.session.add(newUser)
        try:
            db.session.commit()
        except:
            return {'message': 'Username or Email have been used!'}, 400, {'Content-Type': 'application/json'}
        return marshal(newUser, Users.Users_fields), 200, {'Content-Type': 'application/json'}
 
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.get(claims['id'])
        if qry is None:
            return {'message': 'Data not found'}, 204, {'Content-Type': 'application/json'}
        return marshal(qry, Users.Users_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        qry = Users.query.get(claims['id'])
        parse = reqparse.RequestParser()
        if qry is None:
            return {'message': 'Data not found'}, 404, {'Content-Type': 'application/json'}
        parse.add_argument('email', location='json')
        parse.add_argument('password', location='json')
        args = parse.parse_args()

        qry.email = args['email'] if args['email'] is not None else qry.email
        if args['password'] is not None:
            validation = self.policy.test(args['password'])
            if validation:
                errorList = []
                for item in validation:
                    split = str(item).split('(')
                    error, num = split[0], split[1][0]
                    errorList.append("{err}(minimum {num})".format(err=error, num=num))
                message = "Please check your password: " + ', '.join(x for x in errorList)
                return {'message': message}, 422, {'Content-Type': 'application/json'}
            encrypted = hashlib.md5(args['password'].encode()).hexdigest()
            qry.password = encrypted
        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, Users.Users_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @admin_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'message': 'Data not found'}, 404, {'Content-Type': 'application/json'}
        db.session.delete(qry)
        try:
            db.session.commit()
        except:
            return {'message': 'Error deleting!'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, Users.Users_fields), 200, {'Content-Type': 'application/json'}

    def options(self, id=None):
        return {'status': 'OK'}, 200

class UserList(Resource):
    @jwt_required
    @admin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('username', location='args')
        parser.add_argument('orderby', location='args', help='Invalid orderby value', choices=('username', 'email', 'id'))
        parser.add_argument('sort', location='args', help='Invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        qry = Users.query
        
        qry = qry.filter(Users.username.like("%"+args['username']+"%")) if args['username'] is not None else qry

        if args['orderby'] is not None:
            orderby = 'Users.'+str(args['orderby'])
            if args['sort'] is not None and args['sort']=='desc':
                orderby = str(args['sort'])+'('+'Users.'+str(args['orderby'])+')'
            qry = qry.order_by(eval(orderby))
        
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            qry2 = User_Details.query.filter_by(user_id=row.id).first()
            details = marshal(qry2, User_Details.User_Details_fields)
            user = marshal(row, Users.Users_fields)
            user['details'] = details
            user['name']= qry2.fname+' '+qry2.lname if qry2 is not None else user['email']
            rows.append(user)
        if not rows:
            return {'message': 'No user found'}, 404, {'Content-Type': 'application/json'}
        return rows, 200

    def options(self):
        return {'status': 'OK'}, 200

class UserOrder(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = Order.query
        qry = qry.filter_by(user_id=claims['id'])
        rows = []
        for row in qry.all():
            rows.append(marshal(row, Order.Order_fields))
        if not rows:
            return {'message': 'No Order have been made yet'}, 404, {'Content-Type': 'application/json'}
        return rows, 200

    def options(self):
        return {'status': 'OK'}, 200

api.add_resource(UserResource, '', '/<id>')
api.add_resource(UserList, '/list')
api.add_resource(UserOrder, '/order')