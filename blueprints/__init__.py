from flask import Flask, request
import json

##database import###
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import Manager

##JWT import
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta

#wraps import
from functools import wraps

# CORS import
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['APP_DEBUG'] = True

#################
###### JWT ######
#################

app.config['JWT_SECRET_KEY'] = 'Sfasdlah8xPnS73nS3dhb'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['client_type'] != 'admin'  :
            return {'status':'FORBIDDEN', 'message':'User Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def shop_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        
        verify_jwt_in_request()
        claims = get_jwt_claims()
        #import model
        from blueprints.user.model import Users
        qry_user = Users.query.get(claims['id'])
        if qry_user.client_type != 'seller':
            return {'status':'FORBIDDEN', 'message':'USER DON\'T HAS SHOP'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


#################
####Database#####
#################

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://alta123:h@localhost:3306/eCommerce_project'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fikriamri:threecheers@localhost:3306/pair_project'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)  # command 'db' dapat menjalankan semua command MigrateCommand


##################################
###########Middleware#############
##################################

@app.after_request
def after_request(response):   
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    app.logger.warning("REQUEST_LOG\t%s", 
        json.dumps({
            'uri':request.full_path,
            'code':response.status,
            'method':request.method,
            'request':requestData,
            'response':json.loads(response.data.decode('utf-8'))}))

    return response

###############################
###### Import blueprints ######
###############################

from blueprints.auth import bp_auth
from blueprints.user.resources import bp_user
from blueprints.product.resources import bp_product
from blueprints.shop.resources import bp_shop
from blueprints.cart.resources import bp_cart
from blueprints.order.resources import bp_order
from blueprints.category.resources import bp_category
from blueprints.methodPayment.resources import bp_methodPayment
from blueprints.orderDetail.resources import bp_orderDetails

app.register_blueprint(bp_auth, url_prefix='')
app.register_blueprint(bp_user, url_prefix='/users' )
app.register_blueprint(bp_product, url_prefix='/product')
app.register_blueprint(bp_shop, url_prefix='/shop')
app.register_blueprint(bp_cart, url_prefix='')  ## product/<id>/cart
app.register_blueprint(bp_order, url_prefix='')  ## product/<id>/cart
app.register_blueprint(bp_category, url_prefix='/category')  ## product/<id>/cart
app.register_blueprint(bp_methodPayment, url_prefix='/methodpayment')
app.register_blueprint(bp_orderDetails, url_prefix='/orderdetails')



# db.create_all()