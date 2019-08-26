from blueprints import db
from flask_restful import fields

from datetime import datetime

#################
#Table user(pelapak dan pembeli)
#################

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_key = db.Column(db.String(30), unique=True, nullable=False)
    client_secret = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    product_order_cnt = db.Column(db.Integer, nullable=True, default=0)
    status = db.Column(db.String(10), nullable=False, default='inactive')
    client_type = db.Column(db.String(10), nullable=False, default='user')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    response_field = {
        'id': fields.Integer,
        'client_key':fields.String,
        'client_secret':fields.String,
        'address': fields.String,
        'contact': fields.String,
        'product_order_cnt': fields.Integer,
        'status': fields.String,
        'created_at':fields.DateTime 
    }

    claim_response_field = {
        'id': fields.Integer,
        'client_key':fields.String,
        'client_type':fields.String
    }

    def __init__(self,client_key, client_secret, address, contact):
        self.client_key = client_key
        self.client_secret = client_secret
        self.address = address
        self.contact = contact

    def __repr__(self):
        return '<user %r>' % self.id


