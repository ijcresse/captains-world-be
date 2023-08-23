import secrets
from datetime import datetime, timedelta

from flask import Blueprint, request, session, current_app
from .route_util import create_response, current_milli_time
from services.db import get_db, close_db
from models.user import User

users_api = Blueprint('user', __name__, url_prefix = '/api/user')

#TODO:
#create test user in db x
#check login success x
#check login username fail x
#check login password fail x
#check logout with real session x
#check logout with no session x
#check session verify with real session x
#check session verify without real session x
#check session verify with expired session
#check multiple active sessions verify (this... actually seems tough. how do i do this?)
#probably need a cleanup script to get rid of dangling sessions (relogging in, for example)

#POST login
#verifies login against encrypted credentials and sets a session cookie for valid users
@users_api.route("/login", methods=['POST'])
def login():
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
        
        session['username'] = session_name

        return create_response(status = 200, desc = "successful login")
    else:
        close_db(c)
        return create_response(status = 401, desc = "invalid username or password")
    

@users_api.route("/logout")
def logout():
    session_name = session.pop('username', None)

    if session_name is None:
        return create_response(status = 204)

    c = get_db()
    successful_deletion = delete_session(session_name, c)

    if successful_deletion:
        return create_response(status = 200, desc = 'logged out')
    else:
        #no session found, user is effectively logged out already
        return create_response(status = 204)
    
@users_api.route("/session", methods=['POST'])
def verify_session():
    if 'username' in session:
        session_name = session['username']
        c = get_db()
        cursor = c.cursor()
        query = User.fetch_session(session_name)
        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            close_db(c)
            return create_response(401, desc = 'missing session')
        else:
            if session_is_active(result['c_login_time']):
                return create_response(status = 200, desc = f'active session')
            else:
                delete_session(session_name, c)
                return create_response(status = 401, desc = f'expired session')
    return create_response(status = 401, desc = 'missing session')

#deletes an active session. assumed to be last operation, closes connection
def delete_session(session_name, c):
    cursor = c.cursor()
    query = User.fetch_session(session_name)
    cursor.execute(query)
    result = cursor.fetchone()

    #no session found, no operation
    if result is None:
        close_db(c)
        return False
    else:
        query = User.delete_session(result['c_id'])
        cursor.execute(query)
        c.commit()
        close_db(c)
        return True

def session_is_active(login_time):
    login_duration_env = current_app.config['DB']['session_timeout']
    login_duration = datetime.strptime(login_duration_env, '%H:%M:%S')
    logout_time = login_time + timedelta(hours = login_duration.hour)
    current_time = datetime.now()
    return logout_time > current_time