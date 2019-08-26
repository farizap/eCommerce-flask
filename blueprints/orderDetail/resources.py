from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app, shop_required
from sqlalchemy import desc

## JWT IMPORT
from flask_jwt_extended import jwt_required, get_jwt_claims

## model import
from .model import OrderDetails
from blueprints.product.model import Products
from blueprints.shop.model import Shops
from blueprints.order.model import Orders
from blueprints.user.model import Users
from blueprints.userDetail.model import UsersDetail


bp_orderDetails = Blueprint('orderDetails', __name__)
api = Api(bp_orderDetails)

class ShopOrdersGetListResource(Resource):
    def options(self):
        return {"status":"ok"}, 200

    @shop_required
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp',type=int, location='args', default=25)
        parser.add_argument('filter_by', location='args',choices=('id','name'))
        parser.add_argument('order_by', location='args',choices=('price','stock'))
        parser.add_argument('sort', location='args',choices=('asc','desc'))
        args = parser.parse_args()

        claims = get_jwt_claims()

        qry_shop = Shops.query.filter_by(users_id=claims['id']).limit(1).first()
        qry_product = Products.query.filter_by(shop_id=qry_shop.id)

        if qry_product.first() is None:
            return {'No product sell Yet'}, 404            
        results = []
        for product in qry_product.all():
            result = {}
            result['product'] = marshal(product, Products.response_field)
            qry_orderdetails = OrderDetails.query.filter_by(product_id=product.id).all()
            orderDetailList = []
            for orderdetail in qry_orderdetails:
                qry_order = Orders.query.get(orderdetail.order_id)
                qry_user = Users.query.get(qry_order.user_id)
                qry_userDetail = UsersDetail.query.filter_by(users_id = qry_user.id).first()
                orderdetail_temp = marshal(orderdetail, OrderDetails.response_field)
                orderdetail_temp['buyer'] = marshal(qry_user,Users.response_field)
                orderdetail_temp['buyer_detail'] = marshal(qry_userDetail, UsersDetail.response_field)

                orderDetailList.append(orderdetail_temp)
            result['orderDetails'] = orderDetailList
            results.append(result)
        
        return results , 200


api.add_resource(ShopOrdersGetListResource, '/shop/me')
