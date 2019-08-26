from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app, shop_required
from sqlalchemy import desc

## JWT IMPORT
from flask_jwt_extended import jwt_required, get_jwt_claims

## Model import
from .model import Products
from blueprints.category.model import Category
from blueprints.shop.model import Shops


bp_product = Blueprint('product', __name__)
api = Api(bp_product)


class ProductResourceList(Resource):
    def options(self):
        return {"status":"ok"}, 200
        
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('category_id',location='args',type=int, help='invalid status')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('name','price',"created_at",'buy_count'))
        parser.add_argument('sort',location='args',help='invalid sort', choices=('desc','asc'))
        parser.add_argument('search',location='args')
        args =parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Products.query.filter_by(status = 'Ready')

        if args['orderby'] is not None:
            if args['orderby'] == 'name':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.name))
                else:
                    qry = qry.order_by(Products.name)
            elif args['orderby'] == 'price':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.price))
                else:
                    qry = qry.order_by(Products.price)
            elif args['orderby'] == 'created_at':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.created_at))
                else:
                    qry = qry.order_by(Products.created_at)
            elif args['orderby'] == 'buy_count':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.buy_count))
                else:
                    qry = qry.order_by(Products.buy_count)

        if args['search'] is not None:
            qry= qry.filter(Products.name.like('%' +args['search'] + '%'))

        if args['category_id'] is not None:
            qry = qry.filter_by(category_id=args['category_id'])

        result = []
        for row in qry.limit(args['rp']).offset(offset).all():
            result.append(marshal(row,Products.response_field))

        return result, 200, {'Content-Type':'application/json'}

class ProductResource(Resource):
    def options(self, id = 0):
        return {"status":"ok"}, 200

    # user input new product
    @jwt_required
    @shop_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category_id', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('img_url', location='json')
        parser.add_argument('stock', type=int, location='json')
        parser.add_argument('price', type=int, location='json')
        parser.add_argument('description', location='json')
        data = parser.parse_args()

        claims = get_jwt_claims()
        if data['stock'] <0:
            return {'message' : 'invalid stock input'}, 400
        elif data['stock'] > 0:
            status = 'Ready'
        else:
            status = 'Out of Stock'
        
        # edit user table
        qry_shop = Shops.query.filter_by(users_id=claims['id']).limit(1).first()
        qry_shop.product_cnt += 1
        qry_shop.status = 'active'

        product = Products(data['category_id'], qry_shop.id, data['name'],data['img_url'],data['stock'], data['price'], status, data['description'])
        db.session.add(product)

        db.session.commit()
        return marshal(product, Products.response_field), 200
        
    def get(self,id):
        qry_product = Products.query.get(id)

        if qry_product is None:
            return {"status" : "NOT FOUND"}, 404
        
        return marshal(qry_product, Products.response_field), 200

    @jwt_required
    @shop_required
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('category_id', location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('img_url', location='json')
        parser.add_argument('stock', type=int, location='json')
        parser.add_argument('price', type=int, location='json')
        parser.add_argument('description', location='json')
        data = parser.parse_args()

        claims = get_jwt_claims()
        qry_shop = Shops.query.filter_by(users_id=claims['id']).first()

        qry_product = Products.query.get(id)

        if qry_product is None:
            return {"status" : "NOT FOUND"}, 404
        elif qry_product.shop_id != qry_shop.id:
            return {"status" : "UNAUTHORIZED"}, 401

        if data['stock'] <0:
            return {'message' : 'invalid stock input'}, 400
        elif data['stock'] > 0:
            status = 'Ready'
        else:
            status = 'Out of Stock'

        if data['category_id'] is not None:
            qry_product.category_id = data['category_id']
        if data['name'] is not None:
            qry_product.name = data['name']
        if data['img_url'] is not None:
            qry_product.img_url = data['img_url']
        if data['stock'] is not None:
            qry_product.stock = data['stock']
        if data['price'] is not None:
            qry_product.price = data['price']
            
        if data['description'] is not None:
            qry_product.description = data['description']

        qry_product.status = status

        db.session.commit()

        return marshal(qry_product,Products.response_field), 200

    @jwt_required
    @shop_required
    def delete(self,id):
        claims = get_jwt_claims()
        qry_product = Products.query.get(id)

        qry_shop = Shops.query.filter_by(users_id=claims['id']).limit(1).first()

        if qry_product is None:
            return {"status" : "NOT FOUND"}, 404
        elif qry_product.shop_id != qry_shop.id:
            return {"status" : "UNAUTHORIZED"}, 401

        db.session.delete(qry_product)
        db.session.commit()

        return {'status':'DELETED'}, 200


class ShopItemsResource(Resource):
    def options(self):
        return {"status":"ok"}, 200
    # user get all product sold by the user
    @jwt_required
    @shop_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('filter_by', location='args',choices=('id','name'))
        parser.add_argument('order_by', location='args',choices=('price','stock'))
        parser.add_argument('sort', location='args',choices=('asc','desc'))
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_shop = Shops.query.filter_by(users_id=claims['id']).limit(1).first()

        qry_product = Products.query.filter_by(shop_id= qry_shop.id).all()

        result = marshal(qry_shop, Shops.response_field)
        result['products'] = marshal(qry_product,Products.response_field)

        return result, 200


# class ShopItemsDetailResource(Resource):
    # def options(self,id):
    #     return {"status":"ok"}, 200
    # @jwt_required
    # @shop_required
    # def get(self,id):

    #     claims = get_jwt_claims()
    #     qry_product = Products.query.get(id)
    #     qry_shop = Shops.query.filter_by(users_id=claims['id']).first()

    #     if qry_product is None:
    #         return {"status" : "NOT FOUND"}, 404
    #     elif qry_product.shop_id != qry_shop.id:
    #         return {"status" : "UNAUTHORIZED"}, 401
        
    #     return marshal(qry_product, Products.response_field), 200
    
   


api.add_resource(ProductResourceList,'/all')
api.add_resource(ProductResource,'','/<id>')
api.add_resource(ShopItemsResource,'/shop')
# api.add_resource(ShopItemsDetailResource,'/shop/<id>')