from blueprints import db
from datetime import datetime
from flask_restful import fields

class Order_Details(db.Model):
    __tablename__='Order_Details'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id', ondelete='SET NULL'), nullable=True)
    qty = db.Column(db.Integer, nullable=False, default=1)
    tot_price = db.Column(db.Float, nullable=False, default=0)

    Order_Details_fields = {
        'id': fields.Integer,
        'order_id': fields.Integer,
        'product_id': fields.Integer,
        'qty': fields.Integer,
        'tot_price': fields.Float
    }

    def __init__(self, order_id, product_id, qty, tot_price):
        self.order_id = order_id
        self.product_id = product_id
        self.qty = qty
        self.tot_price = tot_price