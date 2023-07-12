from flask import Blueprint

api = Blueprint('api', __name__)

def create_response(status, desc = "", data = []):
    return { 'status': status, 'desc' : desc, 'data': data }

@api.route("/health", methods=['GET'])
def health():
    return create_response(status = 200, desc = "OK")

@api.route("/availability", methods=['GET'])
def availability():
    return create_response(status = 200, desc = "OK")