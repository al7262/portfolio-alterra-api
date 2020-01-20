from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims, get_raw_jwt
from ..user.resources import Users
from ..user_details.resources import User_Details
from ..address.resources import Address
from password_strength import PasswordPolicy
import hashlib
from blueprints import admin_required, db

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class LoginUser(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        if args['username']=='admin' and args['password']=='admin123':
            token = create_access_token(identity = args['username'], user_claims = {'id': 0, 'username': args['username'], 'admin': True})
            return {'token': token}, 200
        
        encrypted = hashlib.md5(args['password'].encode()).hexdigest()
        qry = Users.query.filter_by(username=args['username']).filter_by(password=encrypted)
        clientData = qry.first()
        if clientData is not None:
            clientData = marshal(clientData, Users.jwt_fields)
            clientData['admin'] = False
            token = create_access_token(identity = clientData['id'], user_claims = clientData)
            return {'token': token}, 200
        return {'status': 'UNAUTHORIZED', 'message': 'Invalid username or password'}, 401
    
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200

    def options(self, id=None):
        return {'status': 'OK'}, 200

class RefreshToken(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token': token}, 200

    def options(self, id=None):
        return {'status': 'OK'}, 200

api.add_resource(LoginUser, '/login')
api.add_resource(RefreshToken, '/refresh')