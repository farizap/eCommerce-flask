from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app, admin_required
from sqlalchemy import desc
from .model import MethodPayment

# JWT import
from flask_jwt_extended import jwt_required

bp_methodPayment = Blueprint('methodPayment', __name__)
api = Api(bp_methodPayment)

class MethodPaymentResources(Resource):
    def options(self):
        return {"status":"ok"}, 200

    @admin_required
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('no_rek', location='json', required=True)
        parser.add_argument('name_rek', location='json', required=True)
        data = parser.parse_args()

        methodPayment = MethodPayment(data['name'], data['no_rek'], data['name_rek'])
        db.session.add(methodPayment)
        db.session.commit()

        return marshal(methodPayment, MethodPayment.response_field), 200

    @admin_required
    @jwt_required
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('no_rek', location='json', required=True)
        parser.add_argument('name_rek', location='json', required=True)
        data = parser.parse_args()

        qry_methodPayment = MethodPayment.query.get(id)

        if qry_methodPayment is None:
            return {"status": "Id not found"}, 404

        if data['name'] is not None:
            qry_methodPayment.name = data['name']
        if data['no_rek'] is not None:
            qry_methodPayment.no_rek = data['no_rek']
        if data['name_rek'] is not None:
            qry_methodPayment.name_rek = data['name_rek']

        db.session.commit()

        return marshal(qry_methodPayment, MethodPayment.response_field), 200
    
    def get(self,id):

        qry = MethodPayment.query.get(id)

        if qry is None:
            return {'status':'id not found'}, 404
        # result = []
        # for row in qry.all():
        #     result.append(marshal(row, MethodPayment.response_field))

        return marshal(qry,MethodPayment.response_field), 200, {'Content-Type': 'application/json'}

    @admin_required
    @jwt_required
    def delete(self, id):
        qry_methodPayment = MethodPayment.query.get(id)

        if qry_methodPayment is None:
            return {"status": "CART EMPTY"}, 404

        db.session.delete(qry_methodPayment)
        db.session.commit()
        return {'status': 'DELETED'}, 200

class MethodPaymentResourcesGet(Resource):
    def options(self,id):
        return {"status":"ok"}, 200

    def get(self):

        qry = MethodPayment.query

        qry = qry.order_by(MethodPayment.name)

        result = []
        for row in qry.all():
            result.append(marshal(row, MethodPayment.response_field))

        return result, 200, {'Content-Type': 'application/json'}

api.add_resource(MethodPaymentResources,'', '/<id>', )
api.add_resource(MethodPaymentResourcesGet, '/list')