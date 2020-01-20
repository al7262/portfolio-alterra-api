from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app, admin_required
from .model import Category
from datetime import datetime
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
import hashlib

bp_category = Blueprint('Category', __name__)
api = Api(bp_category)

class CategoryResource(Resource):
    def get(self, id):
        qry = Category.query.get(id)
        if qry is None:
            return {'message': 'Category is not found'}, 404, {'Content-Type': 'application/json'}
        return marshal(qry, Category.Category_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @admin_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('name', location='json', required=True)
        parse.add_argument('description', location='json', required=True)
        args = parse.parse_args()

        newCategory = Category(args['name'], args['description'])
        db.session.add(newCategory)
        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return marshal(newCategory, Category.Category_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @admin_required
    def put(self, id):
        qry = Category.query.get(id)
        if qry is None:
            return {'message': 'Category is not found'}, 404, {'Content-Type': 'application/json'}
        parse = reqparse.RequestParser()
        parse.add_argument('name', location='json')
        parse.add_argument('description', location='json')
        args = parse.parse_args()

        qry.name = args['name'] if args['name'] is not None else qry.name
        qry.description = args['description'] if args['description'] is not None else qry.description
        
        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, Category.Category_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @admin_required
    def delete(self, id):
        qry = Category.query.get(id)
        if qry is None:
            return {'message': 'Data not found'}, 404, {'Content-Type': 'application/json'}
        db.session.delete(qry)
        db.session.commit()
        category = marshal(qry, Category.Category_fields)
        return {'Category': category, 'message': 'Category deleted!'}, 200, {'Content-Type': 'application/json'}

    def options(self, id=None):
        return {'status': 'OK'}, 200

class CategoryList(Resource):
    def get(self):
        qry = Category.query
        rows = []
        for row in qry.all():
            rows.append(marshal(row, Category.Category_fields))
        if not rows:
            return {'message': 'Category is not found'}, 404, {'Content-Type': 'application/json'}
        return rows, 200

    def options(self):
        return {'status': 'OK'}, 200

api.add_resource(CategoryResource, '', '/<id>')
api.add_resource(CategoryList, '/list')