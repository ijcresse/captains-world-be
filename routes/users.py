import secrets

from flask import Blueprint, request, session, current_app
from .route_util import is_authorized, unauthorized_response, delete_session, build_cors_preflight_response, make_cors_response
from services.db import get_db, close_db
from models.user import User

users_api = Blueprint('user', __name__, url_prefix = '/api/user')

#POST login
#verifies login against encrypted credentials and sets a session cookie for valid users
@users_api.route("/login", methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response(request.origin)

    res = make_cors_response(request.origin)

    if request.is_json is False:
        res.status = 400
        res.set_data('Missing login data')
        return res

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
            res.status = 500
            res.set_data('Failed to create a valid session')
            return res
        finally:
            close_db(c)
        
        session['cw-session'] = session_name
        one_day = 60 * 60 * 24
        res.set_cookie('cw-session', session_name,
                        max_age=one_day,
                        path='/',
                        secure=current_app.config['SESSION_COOKIE_SECURE'],
                        samesite=current_app.config['SESSION_COOKIE_SAMESITE']) # this should pull from current_app.config
        return res
    else:
        close_db(c)
        res.status = 401
        res.set_data('Failed to validate credentials')
        return res

@users_api.route("/logout", methods=['GET', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response(request.origin)
    
    res = make_cors_response(request.origin)

    session_name = session.pop('cw-session', None)

    if session_name is None:
        res.status = 204
        return res

    c = get_db()
    successful_deletion = delete_session(session_name, c)

    if successful_deletion:
        return res
    else:
        #user is effectively logged out anyway. no content = no action
        res.status = 204
        return res
    
@users_api.route("/session", methods=['GET', 'OPTIONS'])
def verify_session():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response(request.origin)
    
    res = make_cors_response(request.origin)
    c = get_db()
    cursor = c.cursor()

    if is_authorized(cursor) is False:
        res = unauthorized_response(res)
        
    close_db(c)
    return res
