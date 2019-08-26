from blueprints import db
from flask_restful import fields

from datetime import datetime

#################
#Table Order dan Order detail
#################

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('methodPayment.id'),nullable=False)
    total_product = db.Column(db.Integer,nullable=False, default=0)
    total_qty = db.Column(db.Integer,nullable=False, default=0)
    total_price = db.Column(db.Integer,nullable=False, default=0)
    # created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    response_field = {
        'id': fields.Integer,
        'user_id':fields.Integer,
        'payment_id':fields.Integer,
        'total_product':fields.Integer,
        'total_qty': fields.Integer,
        'total_price': fields.Integer
    }

    def __init__(self,user_id,payment_id,total_product,total_qty, total_price):
        self.user_id = user_id
        self.payment_id = payment_id
        self.total_product = total_product
        self.total_qty = total_qty
        self.total_price = total_price

    def __repr__(self):
        return '<order %r>' % self.id

