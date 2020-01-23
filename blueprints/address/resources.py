from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app, admin_required
from .model import Address
from blueprints.user.model import Users
from datetime import datetime
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
import hashlib

bp_address = Blueprint('Address', __name__)
api = Api(bp_address)

class AddressResource(Resource):
    @jwt_required
    def get(self, id):
        claims = get_jwt_claims()
        qry = Address.query.get(id)
        if qry is None:
            return {'message': 'Address is not found'}, 404, {'Content-Type': 'application/json'}
        if qry.user_id is not claims['id']:
            return {'message': 'You are not authorized'}, 403, {'Content-Type': 'application/json'}
        return marshal(qry, Address.Address_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('contact', location='json', required=True)
        parse.add_argument('details', location='json', required=True)
        parse.add_argument('city', location='json', required=True)
        parse.add_argument('province', location='json', required=True)
        parse.add_argument('zipcode', location='json', required=True)
        args = parse.parse_args()

        qry = Users.query.get(claims['id'])
        user = marshal (qry, Users.Users_fields)

        newAddress = Address(user['id'], args['contact'], args['details'], args['city'], args['province'], args['zipcode'])
        db.session.add(newAddress)
        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again!'}, 400, {'Content-Type': 'application/json'}
        return marshal(newAddress, Address.Address_fields),200,{'Content-Type': 'application/json'}

    @jwt_required
    def put(self, id):
        claims = get_jwt_claims()
        qry = Address.query.get(id)
        if qry is None:
            return {'message': 'Address is not found'}, 404, {'Content-Type': 'application/json'}
        if qry.user_id is not claims['id']:
            return {'message': 'You are not authorized'}, 403, {'Content-Type': 'application/json'}

        parse = reqparse.RequestParser()
        parse.add_argument('contact', location='json')
        parse.add_argument('details', location='json')
        parse.add_argument('city', location='json')
        parse.add_argument('province', location='json')
        parse.add_argument('zipcode', location='json')
        args = parse.parse_args()

        qry.contact = args['contact'] if args['contact'] is not None else qry.contact
        qry.details = args['details'] if args['details'] is not None else qry.details
        qry.city = args['city'] if args['city'] is not None else qry.city
        qry.province = args['province'] if args['province'] is not None else qry.province
        qry.zipcode = args['zipcode'] if args['zipcode'] is not None else qry.zipcode

        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again!'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, Address.Address_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, id):
        claims = get_jwt_claims()
        qry = Address.query.get(id)
        if qry is None:
            return {'message': 'Address is not found'}, 404, {'Content-Type': 'application/json'}
        if qry.user_id is not claims['id']:
            return {'message': 'You are not authorized'}, 403, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()
        address = marshal(qry, Address.Address_fields)
        return {'address': address, 'message': 'Address deleted!'}, 200, {'Content-Type': 'application/json'}

    def options(self, id=None):
        return {'status': 'OK'}, 200

class AddressList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = Address.query
        qry = qry.filter_by(user_id=claims['id'])
        rows = []
        for row in qry.all():
            rows.append(marshal(row, Address.Address_fields))
        if not rows:
            return {'message': 'No address have been inputted yet'}, 404, {'Content-Type': 'application/json'}
        totalQry = len(qry.all())
        return {'total':totalQry, 'result':rows}, 200

    def options(self):
        return {'status': 'OK'}, 200

api.add_resource(AddressResource, '', '/<id>')
api.add_resource(AddressList, '/list')
