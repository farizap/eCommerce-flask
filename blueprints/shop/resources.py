from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc

## JWT IMPORT
from blueprints import shop_required
from flask_jwt_extended import jwt_required, get_jwt_claims

## Model import
from .model import Shops
from blueprints.product.model import Products
from blueprints.user.model import Users

bp_shop = Blueprint('shop', __name__)
api = Api(bp_shop)


class ShopRegisterResource(Resource):
    def options(self):
        return {"status":"ok"}, 200
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required = True)
        parser.add_argument('address', location='json', required = True)
        parser.add_argument('city', location='json', required = True)
        parser.add_argument('contact', type=int, location='json', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        shop = Shops(claims['id'],data['name'],data['city'],data['address'],data['contact'])

        qry_user = Users.query.get(claims['id'])
        qry_user.client_type = 'seller'

        db.session.add(shop)
        db.session.commit()
        return marshal(shop, Shops.response_field), 200


class ShopResource(Resource):
    def options(self,shop_id =0):
        return {"status":"ok"}, 200
    def get(self,shop_id):
        qry_shop = Shops.query.get(shop_id)
        
        if qry_shop is None:
            return {'status':'NOT_FOUND'}, 404

        return marshal(qry_shop, Shops.response_field), 200

    @jwt_required
    @shop_required
    def put(self,shop_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('city', location='json')
        parser.add_argument('contact', type=int, location='json')
        data = parser.parse_args()


        claims = get_jwt_claims()

        qry_shop = Shops.query.get(shop_id)
        if qry_shop.users_id != claims['id']:
            return {'status':'NOT YOUR SHOP'}, 404

        if data['name'] is not None:
            qry_shop.name = data['name']
        if data['address'] is not None:
            qry_shop.address = data['address']
        if data['contact'] is not None:
            qry_shop.contact = data['contact']
        if data['city'] is not None:
            qry_shop.city = data['city']
    
        db.session.commit()

        return {'status' : 'Modified'}, 200, {'Content-Type':'application/json'}

    @jwt_required
    @shop_required
    def delete(self,shop_id):
        claims = get_jwt_claims()

        qry_shop = Shops.query.get(shop_id)
        if qry_shop.users_id != claims['id']:
            return {'status':'NOT YOUR SHOP'}, 404

        qry_users = Users.query.get(claims['id'])
        qry_users.client_type = 'user'
        db.session.delete(qry_shop)
        db.session.commit()

# class ShopListResource(Resource):
    # def get(self):


api.add_resource(ShopRegisterResource,'/register')
api.add_resource(ShopResource,'','/<shop_id>')



