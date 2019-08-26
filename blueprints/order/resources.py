from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app, shop_required
from sqlalchemy import desc

## JWT IMPORT
from flask_jwt_extended import jwt_required, get_jwt_claims

## Model import
from blueprints.product.model import Products
from blueprints.user.model import Users
from .model import Orders
from blueprints.orderDetail.model import OrderDetails
from blueprints.cart.model import Carts
from blueprints.methodPayment.model import MethodPayment

bp_order = Blueprint('order', __name__)
api = Api(bp_order)

class OrderResource(Resource):
    def options(self):
        return {"status":"ok"}, 200
        
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('payment_method_id', location='json', required=True)
        data = parser.parse_args()
        claims = get_jwt_claims()
    
        qry_cart = Carts.query.filter_by(user_id=claims['id'])

        if qry_cart.first() is None:
            return {"status":"cart empty"},400 

        total_price = 0
        total_qty = 0
        total_product = 0

        for item in qry_cart.all():
            total_price += item.price
            total_qty += item.qty
            total_product += 1
        
        order = Orders(claims['id'],data["payment_method_id"],total_product, total_qty, total_price)
        db.session.add(order)

        qry_user = Users.query.get(claims['id'])
        qry_user.product_order_cnt += total_product
        if qry_user.status == 'inactive':
            qry_user.status = 'active'

        db.session.commit()
        # shop tambah sell_cnt
        for item in qry_cart.all():
            orderDetails = OrderDetails(item.product_id, order.id, item.qty, item.price)
            qry_product = Products.query.get(item.product_id)
            qry_product.buy_count += item.qty
            qry_product.stock -= item.qty
            if qry_product.stock <=0:
                qry_product.status = 'Out of Stock'
            
            db.session.add(orderDetails)
            db.session.delete(item)

        db.session.commit()
        
        return {'Status' : 'success'}, 200

   
class OrderGetListResource(Resource):
    def options(self):
        return {"status":"ok"}, 200

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('filter_by', location='args',choices=('id','name'))
        parser.add_argument('order_by', location='args',choices=('price','stock'))
        parser.add_argument('sort', location='args',choices=('asc','desc'))
        args = parser.parse_args()

        claims = get_jwt_claims()

        qry_orders = Orders.query.filter_by(user_id=claims['id']).all()
        results = []
        for order in qry_orders:
            result = marshal(order,Orders.response_field)
            qry_paymentMethod = MethodPayment.query.get(order.payment_id)
            result['payment'] = marshal(qry_paymentMethod, MethodPayment.response_field)
            qry_orderDetails = OrderDetails.query.filter_by(order_id=order.id).all()
            listOrderDetails = []
            for orderDetail in qry_orderDetails:
                listOrderDetail = marshal(orderDetail,OrderDetails.response_field)
                
                qry_product = Products.query.get(orderDetail.product_id)
                listOrderDetail['produk'] = marshal(qry_product, Products.response_field)

                listOrderDetails.append(listOrderDetail)
            
            result['orderDetails'] = listOrderDetails
            results.append(result)

        return results , 200




api.add_resource(OrderResource,'/checkout')
api.add_resource(OrderGetListResource,'/order')