from blueprints import db
from datetime import datetime
from flask_restful import fields

class Users(db.Model):
    __tablename__ =  'Users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False) 

    Users_fields = {
        'id': fields.Integer,
        'email': fields.String,
        'username': fields.String,
        'password': fields.String,
    }

    jwt_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String,
    }

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password