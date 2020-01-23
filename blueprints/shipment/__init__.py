from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from datetime import datetime
from sqlalchemy import desc
from blueprints import db, app, admin_required
from datetime import datetime
import json, requests
from flask_jwt_extended import jwt_required, get_jwt_claims

# Creating blueprint
bp_shipment = Blueprint('Shipment', __name__)
api = Api(bp_shipment)
    
API_KEY = '8990a11e8949097b46df6762c56a8331'
COST_API = 'https://api.rajaongkir.com/starter/cost'
CITY_API = 'https://api.rajaongkir.com/starter/city'
PROVINCE_API = 'https://api.rajaongkir.com/starter/province'

class ProvinceResource(Resource):
    def options(self):
        return {'status':'ok'},200

    def get(self):
        req = requests.get(PROVINCE_API, headers={'key': API_KEY})
        result = req.json()
        province_list = result['rajaongkir']['results']
        return {'total':len(province_list), 'result': province_list}, 200

class CityResource(Resource):
    def options(self):
        return {'status':'ok'},200

    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('province', location="args")
        args = parse.parse_args()
        req = requests.get(CITY_API, headers={'key': API_KEY}, params={'province':args['province']})
        result = req.json()
        city_list = result['rajaongkir']['results']
        return {'total':len(city_list), 'result': city_list}, 200

class CostResource(Resource):
    def options(self):
        return {'status':'ok'},200

    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('destination', location="args", required=True)
        parse.add_argument('courier', location="args", required=True)
        args = parse.parse_args()
        data = {
            'origin': 154,
            'destination': args['destination'],
            'courier': args['courier'],
            'weight': 1000
        }
        req = requests.post(COST_API, headers={'key': API_KEY}, json=data)
        result = req.json()
        cost = result['rajaongkir']['results'][0]['costs'][0]['cost'][0]['value']
        return {'total':1, 'result': cost}, 200

    # def GetCityId(self, city):
    #     req = requests.get(self.RAJAONGKIR_CITY_API, params={'key': self.API_KEY})
    #     result = req.json()
    #     city_list = result['rajaongkir']['results']
    #     for city in city_list:
    #         if city['city_name'].lower() == city.lower():
    #             return int(city['city_id'])
    #     return 0

    # def GetBiayaPengiriman(self, kota_asal, kota_tujuan, berat_gram):
    #     """
    #     Calculate shipping costs using the RAJAONGKIR API
    #     """
    #     kota_asal_id = self.GetIdKota(kota_asal)
    #     kota_tujuan_id = self. GetIdKota(kota_tujuan)

    #     req = requests.post(self.RAJAONGKIR_COST_API, json={'key': self. API_KEY, 'origin':kota_asal_id, 'destination':kota_tujuan_id, 'weight':berat_gram, 'courier':self.DEFAULT_COURIER})

    #     result = req.json()

    #     ongkir = result['rajaongkir']['results'][0]['costs'][0]['cost'][0]['value']

    #     return ongkir
    # @jwt_required
    # def get(self):
    #     parse = reqparse.RequestParser()
    #     parse.add_argument('destination', location="json", required=True)
    #     parse.add_argument('courier', location="json", required=True)
    #     args = parse.parse_args()

    #     origin_id = self.GetCityId('Jakarta')
    #     destination_id = self.GetCityId(args['destination'])

    #     data = {
    #         "origin": origin_id,
    #         "destination": destination_id,
    #         "weight": 1000,
    #         "courier": args['courier']
    #     }

    #     req_cost = requests.post(self.COST_API, json=data)
    #     result = req_cost.json()

    #     ongkir = result['rajaongkir']['results'][0]['costs'][0]['cost'][0]['value']

api.add_resource(ProvinceResource, '/province')
api.add_resource(CityResource, '/city')
api.add_resource(CostResource, '/cost')