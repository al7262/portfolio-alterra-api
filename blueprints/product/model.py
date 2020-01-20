from blueprints import db
from datetime import datetime
from flask_restful import fields

class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id', ondelete='SET NULL'), nullable = True)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = True)
    image = db.Column(db.String(1000), nullable = True)
    price = db.Column(db.Float, nullable = False)
    stock = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, server_default = db.func.now()) 
    updated_at = db.Column(db.DateTime, server_default = db.func.now())

    Product_fields = {
        'id': fields.Integer,
        'category_id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'image': fields.String,
        'price': fields.Float,
        'stock': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, category_id, name, description, image, price, stock):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.stock = stock