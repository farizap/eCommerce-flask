from blueprints import db
from flask_restful import fields


#################
#Table Carts
#################

class Carts(db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    qty = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)

    response_field = {
        'id': fields.Integer,
        'product_id':fields.Integer,
        'user_id':fields.Integer,
        'qty': fields.Integer,
        'price': fields.Integer
    }

    def __init__(self,product_id, user_id, qty, price):
        self.product_id = product_id
        self.user_id = user_id
        self.qty = qty
        self.price = price

    def __repr__(self):
        return '<product %r>' % self.id