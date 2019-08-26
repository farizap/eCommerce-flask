from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc

## JWT IMPORT
from flask_jwt_extended import jwt_required, get_jwt_claims

## Model import
from .model import Users
from blueprints.userDetail.model import UsersDetail
from blueprints.product.model import Products
from blueprints.shop.model import Shops

## Resource import
# from blueprints.shop.resources import ShopItemsDetailResource

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserResource(Resource):
    def options(self):
        return {"status":"ok"}, 200
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.get(claims['id'])
        if qry is not None:
            result = marshal(qry, Users.response_field)

            qry_userDetail = UsersDetail.query.filter_by(users_id = claims['id']).first()
            result['Detail'] = marshal(qry_userDetail, UsersDetail.response_field)
            return result, 200
        return {'status':'NOT_FOUND'}, 404


    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_secret', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('contact', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('age',type=int, location='json')
        parser.add_argument('sex', location='json')
        data = parser.parse_args()

        claims = get_jwt_claims()

        qry_users = Users.query.get(claims['id'])
        qry_usersDetail = UsersDetail.query.filter_by(users_id = claims['id']).first()

        if data['client_secret'] is not None:
            qry_users.client_secret = data['client_secret']
        
        if data['address'] is not None:
            qry_users.address = data['address']

        if data['contact'] is not None:
            qry_users.contact = data['contact']
        
        if data['name'] is not None:
            qry_usersDetail.name = data['name']
        
        if data['age'] is not None:
            qry_usersDetail.age = data['age']
        
        if data['sex'] is not None:
            qry_usersDetail.sex = data['sex']

        db.session.commit()

        return {'status' : 'Modified'}, 200, {'Content-Type':'application/json'}


    #  toko masih perlu didilete berserta itemnya
    @jwt_required
    def delete(self):
        
        claims = get_jwt_claims()

        qry_users = Users.query.get(claims['id'])
        qry_usersDetail = UsersDetail.query.filter_by(users_id = claims['id']).first()

        if qry_users is None:
            return {'status':'NOT_FOUND'}, 404

        qry_shop = Shops.query.filter_by(users_id=claims['id']).first()
        if qry_shop is not None:
            qry_product = Products.query.filter_by(shop_id=qry_shop.id).all()
            db.session.delete(qry_shop)
            db.session.commit()
            if qry_product is not None:
                for product in qry_product:
                    db.session.delete(product)
            
        db.session.delete(qry_usersDetail)
        db.session.commit()
        db.session.delete(qry_users)
        
        
        
        db.session.commit()
        return {'status':'DELETED'}, 200


class UserRegisterResource(Resource):
    def options(self):
        return {"status":"ok"}, 200
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('contact', location='json', required=True)
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age',type=int, location='json', required=True)
        parser.add_argument('sex', location='json', choices=('male','female'), required=True)
        data = parser.parse_args()


        user = Users(data['client_key'],data['client_secret'], data['address'], data['contact'])
        db.session.add(user)
        db.session.commit()

        qry_user = Users.query.filter_by(client_key=data['client_key']).first()
        qry_user_srz = marshal(qry_user, Users.response_field)
        user_detail = UsersDetail(qry_user_srz['id'],data['name'],data['age'],data['sex'])
        db.session.add(user_detail)
        db.session.commit()

        return marshal(qry_user, Users.response_field), 200



# class UserRegisterShopResource(Resource):

#     @jwt_required
#     @user_required
#     def post(self):
#         claims = get_jwt_claims()

#         qry_users = Users.query.get(claims['id'])




api.add_resource(UserResource,'/me')
api.add_resource(UserRegisterResource,'/register')



