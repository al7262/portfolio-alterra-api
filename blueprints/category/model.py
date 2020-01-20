from blueprints import db
from datetime import datetime
from flask_restful import fields

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    description = db.Column(db.Text, nullable = True)

    Category_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }

    def __init__(self, name, description):
        self.name = name
        self.description = description