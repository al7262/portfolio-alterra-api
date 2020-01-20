from blueprints import db
from datetime import datetime
from flask_restful import fields

class Order(db.Model):
    __tablename__='Order'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    shipping = db.Column(db.String(50), nullable=True)
    payment = db.Column(db.String(50), nullable=True)
    discount = db.Column(db.Integer, nullable = True, default = 0)
    tot_price = db.Column(db.Float, nullable = False, default = 0)
    shipping_price = db.Column(db.Float, nullable = False, default = 0)
    tot_qty = db.Column(db.Integer, nullable = False, default = 0)
    created_at = db.Column(db.DateTime, server_default = db.func.now()) 
    updated_at = db.Column(db.DateTime, server_default = db.func.now())
    finished = db.Column(db.Boolean, nullable = False, default = False) 

    Order_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'shipping': fields.Integer,
        'payment': fields.Integer,
        'tot_price': fields.Float,
        'shipping_price': fields.Float,
        'tot_qty': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'finished': fields.Boolean
    }

    def __init__(self, user_id, shipping, payment, tot_price, discount, shipping_price, tot_qty, finished):
        self.user_id = user_id
        self.shipping = shipping
        self.payment = payment
        self.tot_price = tot_price
        self.shipping_price = shipping_price
        self.tot_qty = tot_qty
