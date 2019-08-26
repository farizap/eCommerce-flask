from blueprints import db
from flask_restful import fields

from datetime import datetime
#################
#Table Product dan Kategori
#################

class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'),nullable=False)
    name = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.Text, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    buy_count = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(15), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    response_field = {
        'id': fields.Integer,
        'category_id':fields.Integer,
        'shop_id':fields.Integer,
        'img_url' :fields.String,
        'name': fields.String,
        'stock': fields.Integer,
        'price': fields.Integer,
        'buy_count': fields.Integer,
        'status': fields.String,
        'description': fields.String,
        'created_at': fields.DateTime
    }

    def __init__(self,category_id, shop_id, name, img_url, stock, price, status, description):
        self.category_id = category_id
        self.shop_id = shop_id
        self.name = name
        self.img_url = img_url
        self.stock = stock
        self.price = price
        self.status = status
        self.description = description

    def __repr__(self):
        return '<product %r>' % self.id

