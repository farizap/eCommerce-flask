from blueprints import db
from flask_restful import fields

class OrderDetails(db.Model):
    __tablename__ = "orderDetails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'),nullable=False)
    qty = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)

    response_field = {
        'id': fields.Integer,
        'product_id':fields.Integer,
        'order_id':fields.Integer,
        'qty': fields.Integer,
        'price': fields.Integer
    }

    def __init__(self,product_id, order_id, qty, price):
        self.product_id = product_id
        self.order_id = order_id
        self.qty = qty
        self.price = price

    def __repr__(self):
        return '<orderDetail %r>' % self.id