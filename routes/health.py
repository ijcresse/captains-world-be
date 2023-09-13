from flask import Blueprint
from flask_cors import cross_origin
from .route_util import create_response, is_authorized

health_api = Blueprint('health', __name__, url_prefix = '/api')

@health_api.route("/health", methods = ['GET'])
def health():
    return create_response(status = 200, desc = "OK")

@health_api.route("/availability", methods = ['GET'])
def availability():
    return create_response(status = 200, desc = "OK")
