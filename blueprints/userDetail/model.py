from blueprints import db
from flask_restful import fields


class UsersDetail(db.Model):
    __tablename__ = "usersDetail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False,unique=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=True, default=20)
    sex = db.Column(db.String(30), nullable=False)

    response_field = {
        # 'id': fields.Integer,
        # 'users_id':fields.Integer,
        'name': fields.String,
        'age': fields.Integer,
        'sex': fields.String
    }

    def __init__(self,client_id, name, age, sex):
        self.users_id = client_id
        self.name = name
        self.age = age
        self.sex = sex

    def __repr__(self):
        return '<user detail %r>' % self.id
