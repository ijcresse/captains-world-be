import secrets

from flask import Blueprint, request, session, make_response, current_app
#from flask_cors import CORS
from .route_util import create_response, is_authorized, delete_session
from services.db import get_db, close_db
from models.user import User

users_api = Blueprint('user', __name__, url_prefix = '/api/user')
#CORS(users_api, resources = {r'/api/*': {"origins": "http://localhost:5173"}})

def _build_cors_preflight_response():
    res = make_response()
    res.headers.add('Access-Control-Allow-Origin', request.origin)
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    res.headers.add('Access-Control-Allow-Methods', "GET, PUT, POST, OPTIONS")
    res.headers.add('Access-Control-Allow-Headers', 'x-cw-session, Access-Control-Allow-Origin, Access-Control-Allow-Credentials, content-type, content-length')
    res.headers.add('Access-Control-Expose-Headers', 'x-cw-session, Access-Control-Allow-Origin, Access-Control-Allow-Credentials, content-type, content-length')
    return res

#POST login
#verifies login against encrypted credentials and sets a session cookie for valid users
@users_api.route("/login", methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    if request.is_json is False:
        return create_response(status = 401, desc = "Missing login data")

    data = request.get_json()
    user = User(data)

    c = get_db()
    cursor = c.cursor()
    query = user.get_user_query()
    
    cursor.execute(query)
    result = cursor.fetchone()
    valid_login = result is not None and user.check_user(result['c_username'], result['c_password'])

    if valid_login:
        query = user.update_login_query()
        cursor.execute(query)
        c.commit()

        token = secrets.token_urlsafe(32)
        session_name = "captains.world." + token
        query = user.create_session(session_name)
        try:    
            cursor.execute(query)
            c.commit()
        except Exception as e:
            print(f'failed to create session for session {session_name}')
            print(e)
            return create_response(status = 500, desc = "failed to create valid session")
        finally:
            close_db(c)
        
        session['cw-session'] = session_name
        res = make_response()
        one_day = 60 * 60 * 24
        res.set_cookie('cw-session', session_name,
                        max_age=one_day,
                        path='/',
                        secure=current_app.config['SESSION_COOKIE_SECURE'],
                        samesite=current_app.config['SESSION_COOKIE_SAMESITE']) # this should pull from current_app.config
        res.headers.add('Access-Control-Allow-Origin', request.origin)

        #these may be extraneous after the OPTIONS request. clean up when you've got time
        res.headers.add('Access-Control-Allow-Credentials', 'true')
        res.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Origin, Access-Control-Allow-Credentials, content-type, content-length')
        res.headers.add('Access-Control-Expose-Headers', 'Access-Control-Allow-Origin, Access-Control-Allow-Credentials, content-type, content-length')
        res.status = 200
        
        return res
    else:
        close_db(c)
        return create_response(status = 401, desc = "invalid username or password")

@users_api.route("/logout")
def logout():
    session_name = session.pop('cw-session', None)

    if session_name is None:
        return create_response(status = 204)

    c = get_db()
    successful_deletion = delete_session(session_name, c)

    if successful_deletion:
        return create_response(status = 200, desc = 'logged out')
    else:
        #no session found, user is effectively logged out already
        return create_response(status = 204)
    
@users_api.route("/session", methods=['GET'])
def verify_session():
    if is_authorized():
        return create_response(status = 200, desc = f'active session')
    else:
        return create_response(status = 401, desc = 'missing session')
