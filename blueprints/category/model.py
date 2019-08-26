from blueprints import db
from flask_restful import fields


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


    response_field = {
        'id': fields.Integer,
        'name': fields.String
    }

    def __init__(self,name):
        self.name = name


    def __repr__(self):
        return '<category %r>' % self.id
