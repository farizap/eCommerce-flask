from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
import json
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

## import Model
from blueprints.shop.model import Shops
from blueprints.user.model import Users
from flask_restful import fields

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateUserTokenResource(Resource):
    
    def options(self):
        return {"status":"ok"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        
        args = parser.parse_args()

        ###### from database #######
        qry = Users.query

        qry = qry.filter_by(client_key=args['client_key'])
        qry = qry.filter_by(client_secret=args['client_secret']).first()
        
        

        if qry is not None:
            qry_shop = Shops.query.filter_by(users_id=qry.id).first()
            claim = marshal(qry, Users.claim_response_field)
            claim['shop_id'] = marshal(qry_shop, { 'id': fields.Integer,})
            token = create_access_token(identity=args['client_key'], user_claims=claim)
            if qry_shop is None:
                return {'token': token, 'user_id':qry.id, 'user_status':qry.client_type, 'shop_id':""},200
        else:
            return {'status':'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401
        return {'token': token, 'user_id':qry.id, 'user_status':qry.client_type, 'shop_id':qry_shop.id},200

    @jwt_required   # method need auth to run 
    def get(self):
        claims = get_jwt_claims()
        return {'claims':claims}, 200

class RefreshTokenResource(Resource):
    def options(self):
            return {"status":"ok"}, 200
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token':token}, 200


api.add_resource(CreateUserTokenResource,'/login')

api.add_resource(RefreshTokenResource,'/refresh')