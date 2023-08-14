import os

from flask import Blueprint, request, session
from route_util import create_response, get_db, close_db
from models.user import User

users_api = Blueprint('user', __name__, url_prefix = '/api/user')

#make sure this doesn't pull from .env, that just seems like a bad idea
#secret_key = os.getenv('secret_key')

#POST login
#verifies login against encrypted credentials and sets a session cookie for valid users
@users_api.route("/login", methods=['POST'])
def login():
    if request.is_json is False:
        return create_response(status = 401, desc = "Missing login data")

    

    data = request.get_json()
    user = User(data)
    

@users_api.route("/session", methods=['POST'])
def verify_session():
    if 'username' in session:
        return create_response(status = 200, desc = f'logged in as {session["username"]}')
    return create_response(status = 401, desc = 'missing session')