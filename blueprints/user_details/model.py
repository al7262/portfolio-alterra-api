from blueprints import db
from datetime import datetime
from flask_restful import fields

class User_Details(db.Model):
    __tablename__ = 'User_Details'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete = 'CASCADE'), nullable = False)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(200), nullable = True)
    image = db.Column(db.String(1000), nullable = True)
    birth_date = db.Column(db.DateTime, nullable = False)
    gender = db.Column(db.String(10), nullable = True)
    created_at = db.Column(db.DateTime, server_default = db.func.now()) 
    updated_at = db.Column(db.DateTime, server_default = db.func.now())

    User_Details_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'fname': fields.String,
        'lname': fields.String,
        'birth_date': fields.DateTime,
        'gender': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, user_id, fname, lname, image, birth_date, gender):
        self.user_id = user_id
        self.fname = fname
        self.lname = lname
        self.image = image
        self.birth_date = birth_date
        self.gender = gender
