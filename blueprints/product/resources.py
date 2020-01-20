from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from blueprints import db, app, admin_required
from .model import Product
from blueprints.category.model import Category
from datetime import datetime
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
import hashlib

bp_product = Blueprint('Product', __name__)
api = Api(bp_product)


class ProductResource(Resource):
    def get(self, id):
        qry = Product.query.get(id)
        if qry is None:
            return {'message': 'Product is not found'}, 404, {'Content-Type': 'application/json'}
        return marshal(qry, Product.Product_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @admin_required
    def post(self):
        claim = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('name', location='json', required=True)
        parse.add_argument('description', location='json')
        parse.add_argument('image', location='json')
        parse.add_argument('category_id', location='json', required=True)
        parse.add_argument('price', location='json', required=True)
        parse.add_argument('stock', location='json', required=True)
        args = parse.parse_args()

        newProduct = Product(args['category_id'], args['name'], args['description'], args['image'], args['price'], args['stock'])
        db.session.add(newProduct)

        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return marshal(newProduct, Product.Product_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @admin_required
    def put(self, id):
        claims = get_jwt_claims()
        qry = Product.query.get(id)
        if qry is None:
            return {'message': 'Product is not found'}, 404, {'Content-Type': 'application/json'}        

        parse = reqparse.RequestParser()
        parse.add_argument('name', location='json')
        parse.add_argument('description', location='json')
        parse.add_argument('image', location='json')
        parse.add_argument('category_id', location='json')
        parse.add_argument('price', location='json')
        parse.add_argument('stock', location='json')
        args = parse.parse_args()

        qry.name = args['name'] if args['name'] is not None else qry.name
        qry.description = args['description'] if args['description'] is not None else qry.description
        qry.image = args['image'] if args['image'] is not None else qry.image
        qry.category_id = args['category_id'] if args['category_id'] is not None else qry.category_id
        qry.price = args['price'] if args['price'] is not None else qry.price
        qry.stock = args['stock'] if args['stock'] is not None else qry.stock

        try:
            db.session.commit()
        except:
            return {'message': 'Please check your input again'}, 400, {'Content-Type': 'application/json'}
        return marshal(qry, Product.Product_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    @admin_required
    def delete(self, id):
        qry = Product.query.get(id)
        if qry is None:
            return {'message': 'Product is not found'}, 404, {'Content-Type': 'application/json'}
        db.session.delete(qry)
        db.session.commit()
        product = marshal(qry, Product.Product_fields)
        return {'product': product, 'message': 'Product deleted!'}, 200, {'Content-Type': 'application/json'}

    def options(self, id=None):
        return {'status': 'OK'}, 200

class ProductList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('name', location='args')
        parser.add_argument('category_id', location='args')
        parser.add_argument('orderby', location='args', help='Invalid orderby value', choices=('name', 'price', 'created_at'))
        parser.add_argument('sort', location='args', help='Invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        qry = Product.query
        
        qry = qry.filter(Product.name.like("%"+args['name']+"%")) if args['name'] is not None else qry
        qry = qry.filter_by(category_id=args['category_id']) if args['category_id'] is not None else qry

        if args['orderby'] is not None:
            orderby = 'Product.'+str(args['orderby'])
            if args['sort'] is not None and args['sort']=='desc':
                orderby = str(args['sort'])+'('+'Product.'+str(args['orderby'])+')'
            qry = qry.order_by(eval(orderby))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Product.Product_fields))
        if not rows:
            return {'message': 'No product available'}, 404, {'Content-Type':'application/json'}
        return rows, 200

    def options(self):
        return {'status': 'OK'}, 200

api.add_resource(ProductList, '/list')
api.add_resource(ProductResource, '', '/<id>')