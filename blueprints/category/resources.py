from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app, admin_required
from sqlalchemy import desc

# JWT IMPORT
from flask_jwt_extended import jwt_required, get_jwt_claims

# Model import
from .model import Category


bp_category = Blueprint('category', __name__)
api = Api(bp_category)


class CategoryResource(Resource):
    def options(self):
        return {"status":"ok"}, 200


    @admin_required
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        data = parser.parse_args()

        category = Category(data['name'])
        db.session.add(category)
        db.session.commit()

        return marshal(category, Category.response_field), 200

    def get(self, id):

        claims = get_jwt_claims()
        qry_category = Category.query.get(id)

        if qry_category is None:
            return {"status": "NOT FOUND"}, 404

        return marshal(qry_category, Category.response_field), 200

    @admin_required
    @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        data = parser.parse_args()

        qry_category = Category.query.get(id)

        if qry_category is None:
            return {"status": "CART EMPTY"}, 404

        qry_category.name = data['name']
        db.session.commit()
        return marshal(qry_category, Category.response_field), 200

    @admin_required
    @jwt_required
    def delete(self, id):
        qry_category = Category.query.get(id)

        if qry_category is None:
            return {"status": "CART EMPTY"}, 404

        db.session.delete(qry_category)
        db.session.commit()
        return {'status': 'DELETED'}, 200


class CategoryListResouce(Resource):
    def options(self):
        return {"status":"ok"}, 200
    

    def get(self):

        qry = Category.query

        qry = qry.order_by(Category.name)

        result = []
        for row in qry.all():
            result.append(marshal(row, Category.response_field))

        return result, 200, {'Content-Type': 'application/json'}


api.add_resource(CategoryResource, '', '/<id>')
api.add_resource(CategoryListResouce, '/list')
