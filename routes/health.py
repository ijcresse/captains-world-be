from flask import Blueprint
from .route_util import create_response

health_api = Blueprint('health', __name__, url_prefix = '/api')

@health_api.route("/health", methods = ['GET'])
def health():
    print('health route')
    a = 2 + 2
    print(a)
    return create_response(status = 200, desc = "OK")

@health_api.route("/availability", methods = ['GET'])
def availability():
    print('availability route')
    a = 4 + 4
    print(a)
    return create_response(status = 200, desc = "OK")