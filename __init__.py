from datetime import datetime

from flask import Flask

from routes.health import health_api
from routes.drinks import drinks_api
from config import get_env_vars

def create_app():
    app = Flask(__name__)

    print(f"Starting Captain's World Backend Server at {datetime.now()}")
    print(f"Debug Mode: {app.config['DEBUG']}")
    print(f"Session Cookie HTTP Only: {app.config['SESSION_COOKIE_HTTPONLY']}")
    print(f"Session Cookie Secure: {app.config['SESSION_COOKIE_SECURE']}")
    print(f"Secret Key set: {app.config['SECRET_KEY'] is not None}")
    print(f"Bcrypt Salt set: {app.config['BCRYPT_SALT'] is not None}")
    
    cw_dir, cw_db = get_env_vars()
    app.config['DIR'] = cw_dir
    app.config['DB'] = cw_db
    
    app.register_blueprint(health_api)
    app.register_blueprint(drinks_api)

    return app


#GET /drink/search
#queryparams: name year type tags
#tags is own object
#searches drinks and returns paginated list, akin to /drink/list, of drinks that match that criteria

#POST /login
#queryparams: user pass
#returns cookie with creds and valid login if successful.

#POST /drink
#request object: drink_request. full of details and params
#for admin, requires cookie
#stores image elsewhere and fetches image id, stores that in db. unsure exactly how this works.
#ok flask suports this. check under #File-Uploads on their quickstart. includes some details for the HTML form too.

#POST /drink/image
#request object: drink id (?). requires png, jpg, jpeg, gif.
#upload new image 
#i dont like the potential failure of a drink succeeding and an image upload not working.
#one request seems best. 

#PUT /drink/description
#for admin, requires cookie
#updates a given drink with an updated drink object. detects whether image is same. need to figure that one out

#PUT /drink/image
#request object: drink id.
#for updating a drink image.

#PUT /contact
#for admin, requires cookie
#updates contact info for captain

#GET /health
#GET /availability

#POST /login
#POST /register. use scrypt and pbkdf2. good practice here.
#GET /user (verify session)