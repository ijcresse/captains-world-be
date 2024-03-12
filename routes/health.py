from flask import Blueprint, make_response

health_api = Blueprint('health', __name__, url_prefix = '/api')

@health_api.route("/health", methods = ['GET'])
def health():
    res = make_response()
    res.status = 200
    res.set_data("OK")
    return res

@health_api.route("/availability", methods = ['GET'])
def availability():
    res = make_response()
    res.status = 200
    res.set_data("OK")
    return res
