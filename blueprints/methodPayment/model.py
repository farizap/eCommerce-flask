from blueprints import db
from flask_restful import fields


class MethodPayment(db.Model):
    __tablename__ = "methodPayment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30),nullable=False)
    no_rek= db.Column(db.String(30),nullable=False)
    name_rek = db.Column(db.String(30),nullable=False)


    response_field = {
        'id': fields.Integer,
        'name':fields.String,
        'no_rek':fields.String,
        'name_rek':fields.String
    }

    def __init__(self,name,no_rek, name_rek):
        self.name = name
        self.no_rek = no_rek
        self.name_rek = name_rek

    def __repr__(self):
        return '<MethodPayment %r>' % self.id

        