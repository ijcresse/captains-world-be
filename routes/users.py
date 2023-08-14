from flask import Blueprint, request, session, current_app
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

    salt = current_app.config['BCRYPT_SALT']

    data = request.get_json()
    user = User(data, salt)

    c = get_db()
    cursor = c.cursor()
    query = user.get_user_query()
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    print(result)
    valid_login = user.check_user(result['c_username'], result['c_password'])

    if valid_login:
        print(f'setting username: {user.username}')
        session['username'] = user.username

        query = user.update_login_query()
        cursor.execute(query)
        c.commit()
        close_db(c)

        return create_response(status = 200, desc = "successful login")
    else:
        close_db(c)
        return create_response(status = 401, desc = "invalid username or password")
    

@users_api.route("/logout")
def logout():
    session.pop('username', None)
    return create_response(status = 200, desc = 'removed session if exists')

@users_api.route("/session", methods=['POST'])
def verify_session():
    if 'username' in session:
        return create_response(status = 200, desc = f'logged in as {session["username"]}')
    return create_response(status = 401, desc = 'missing session')