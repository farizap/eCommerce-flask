from blueprints import db
from flask_restful import fields

from datetime import datetime
#################
#Table toko(pelapak)
#################

class Shops(db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False,unique=True)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(30), nullable=False)
    reputasi = db.Column(db.Integer, nullable=False, default=0)
    product_cnt = db.Column(db.Integer, nullable=True, default=0)
    status = db.Column(db.String(10), nullable=False, default='Inactive')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    response_field = {
        'id': fields.Integer,
        'users_id':fields.Integer,
        'name': fields.String,
        'address': fields.String,
        'city': fields.String,
        'contact': fields.String,
        'product_cnt': fields.Integer,
        'reputasi' : fields.Integer,
        'status': fields.String,
        'created_at':fields.DateTime 
    }

    def __init__(self,users_id, name,city, address, contact):
        self.users_id = users_id
        self.name = name
        self.city = city
        self.address = address
        self.contact = contact

    def __repr__(self):
        return '<toko %r>' % self.id

