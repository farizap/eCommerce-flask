from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc

## JWT IMPORT
from flask_jwt_extended import jwt_required, get_jwt_claims

## Model import
from blueprints.product.model import Products
from .model import Carts


bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):
    def options(self, id = 0):
            return {"status":"ok"}, 200
    @jwt_required
    def post(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('qty', location='json', type=int, required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()
        qry_product = Products.query.get(id)


        if qry_product is None:
            return {"status" : "NOT FOUND"}, 404
        

        price = qry_product.price * data['qty']
        
        qry_cart = Carts.query.filter_by(product_id=id).first()
        
        if qry_cart is None:
            qry_cart = Carts(id,claims["id"],data['qty'],price)
            
            db.session.add(qry_cart)
        else:
            if qry_product.stock - data['qty']  - qry_cart.qty<= 0 or data['qty'] == 0:
                return {"status" : "qty invalid", "message":"Stock not enough"}, 401 
            qry_cart.price += price
            qry_cart.qty += data['qty']
        db.session.commit()

        return marshal(qry_cart, Carts.response_field), 200

class CartUserResource(Resource):
    def options(self, id=0):
            return {"status":"ok"}, 200
            
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('filter_by', location='args',choices=('id','name'))
        parser.add_argument('order_by', location='args',choices=('price','stock'))
        parser.add_argument('sort', location='args',choices=('asc','desc'))
        args = parser.parse_args()

        claims = get_jwt_claims()
    
        qry_cart = Carts.query.filter_by(user_id=claims['id']).all()
        
        if qry_cart == []:
            return {"status" : "CART EMPTY"}, 200
        

        results = []
        for item in qry_cart:
            result = marshal(item, Carts.response_field)
            qry_product = Products.query.get(result['product_id'])
            result['products'] = marshal(qry_product,Products.response_field)
            results.append(result)

        return results, 200

    @jwt_required
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('qty', location='json', type=int, required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        cart_qry = Carts.query.filter_by(user_id=claims['id'])
        cart_qry = cart_qry.filter_by(id=id).first()

        if cart_qry is None:
            return {"status" : "CART EMPTY"}, 404
        

        cart_qry.qty = data['qty']
        db.session.commit()
        return marshal(cart_qry, Carts.response_field), 200

    @jwt_required
    def delete(self,id):
        

        claims = get_jwt_claims()

        cart_qry = Carts.query.get(id)

        if cart_qry is None:
            return {"status" : "CART EMPTY"}, 404


        db.session.delete(cart_qry)
        db.session.commit()
        return {'status':'DELETED'}, 200


api.add_resource(CartResource,'/product/<id>/cart')
api.add_resource(CartUserResource,'/cart','/cart/<id>')