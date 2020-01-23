from blueprints import db
from datetime import datetime
from flask_restful import fields

class Address(db.Model):
    __tablename__ = 'Address'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete = 'CASCADE'), nullable = False)
    contact = db.Column(db.String(15), nullable = False)
    details = db.Column(db.String(255), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    province = db.Column(db.String(50), nullable = False)
    zipcode = db.Column(db.String(10), nullable = False)

    Address_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'contact': fields.String,
        'details': fields.String,
        'city': fields.String,
        'province': fields.String,
        'zipcode': fields.String
    }

    def __init__(self, user_id, contact, details, city, province, zipcode):
        self.user_id = user_id
        self.contact = contact
        self.details = details
        self.city = city
        self.province = province
        self.zipcode = zipcode
