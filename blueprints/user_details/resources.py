from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app, admin_required
from .model import User_Details
from datetime import datetime
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
import hashlib

bp_user_detail = Blueprint('User_Detail', __name__)
api = Api(bp_user_detail)
      
class UserDetails(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = User_Details.query.filter_by(user_id=claims['id']).first()
        if qry is None:
            return {'message': 'Data is not found'}, 404, {'Content-Type': 'application/json'}
        user = marshal(qry, User_Details.User_Details_fields)
        user['email'] = claims['email']
        user['username'] = claims['username']
        return user, 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        qry = User_Details.query.filter_by(user_id=claims['id']).first()
        if qry is None or qry.deleted:
            return {'message': 'Data not found'}, 404, {'Content-Type': 'application/json'}
        
        parse = reqparse.RequestParser()
        parse.add_argument('fname', location='json')
        parse.add_argument('lname', location='json')
        parse.add_argument('gender', location='json')
        parse.add_argument('image', location='json')
        parse.add_argument('birth_date', location='json')
        args = parse.parse_args()
        
        qry.fname = args['fname'] if args['fname'] is not None else qry.fname
        qry.lname = args['lname'] if args['lname'] is not None else qry.lname
        qry.gender = args['gender'] if args['gender'] is not None else qry.gender
        qry.image = args['image'] if args['image'] is not None else qry.image
        qry.birth_date = args['birth_date'] if args['birth_date'] is not None else qry.birth_date
        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, User_Details.User_Details_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        qry = User_Details.query.filter_by(user_id=claims['id']).first()
      
        parse = reqparse.RequestParser()
        parse.add_argument('fname', location='json', required=True)
        parse.add_argument('lname', location='json', required=False)
        parse.add_argument('gender', location='json', required=True)
        parse.add_argument('image', location='json', required=True)
        parse.add_argument('birth_date', location='json', required=True)
        args = parse.parse_args()
        
        newUserDetails = User_Details(claims['id'], args['fname'], args['lname'], args['image'], args['birth_date'], args['gender'])
        db.session. add(newUserDetails)

        try:
            db.session.commit()
        except:
            return {'message': 'Integrity Error'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, User_Details.User_Details_fields), 200, {'Content-Type': 'application/json'}

    def options(self):
        return {'status': 'OK'}, 200

api.add_resource(UserDetails, '')