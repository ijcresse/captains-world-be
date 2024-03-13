import os
import logging

from datetime import datetime, timedelta
from flask import current_app, jsonify, session, make_response
from werkzeug.utils import secure_filename

from models.user import User
from services.db import get_db, close_db

BEFORE_EXTENSION = 0
AFTER_EXTENSION = 1

#saves an image to disk
def save_image(id, img):
    image_dir = current_app.config['DIR']['images']
    extensions = current_app.config['DIR']['extensions']

    try:
        if allowed_extensions(img.filename, extensions) is False:
            raise Exception("Invalid filename or filetype.")
        filename = secure_filename(f"{id}_{img.filename}")
        img.save(os.path.join(image_dir, filename))
        return filename
    except Exception as error:
        logging.warn(f"Unable to successfully save {filename} to disk.")
        logging.warn(jsonify(error))

def allowed_extensions(filename, extensions):
    allowed = '.' in filename
    if allowed is False:
        return False
    
    extension_split = filename.rsplit('.', 1)
    if len(extension_split[BEFORE_EXTENSION]) == 0:
        return False
    
    return extension_split[AFTER_EXTENSION].lower() in extensions

def is_authorized(cursor):
    if 'cw-session' in session:
        session_name = session['cw-session']
        
        query = User.fetch_session_query(session_name)
        cursor.execute(query)
        result = cursor.fetchone()

        return result and session_is_active(result['c_login_time'])

def session_is_active(login_time):
    current_time = datetime.now()

    login_duration_env = current_app.config['DB']['session_timeout']
    login_duration = datetime.strptime(login_duration_env, '%H:%M:%S')
    logout_time = login_time + timedelta(hours = login_duration.hour)
    
    return logout_time > current_time

#deletes an active session if exists.
def delete_session(session_name, c):
    cursor = c.cursor()
    query = User.fetch_session_query(session_name)
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        query = User.delete_session_query(result['c_id'])
        cursor.execute(query)
        c.commit()

#returns 401 for unauthorized users hitting an auth endpoint
def unauthorized_response(res):
    res.status = 401
    res.set_data("Secured endpoint")
    return res

def build_cors_preflight_response(origin):
    res = make_response()
    res.headers.add('Access-Control-Allow-Origin', origin)
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    res.headers.add('Access-Control-Allow-Methods', "GET, PUT, POST, OPTIONS")
    res.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Origin, Access-Control-Allow-Credentials, content-type, content-length')
    res.headers.add('Access-Control-Expose-Headers', 'Access-Control-Allow-Origin, Access-Control-Allow-Credentials, content-type, content-length')
    return res

def make_cors_response(origin):
    res = make_response()
    res.headers.add('Access-Control-Allow-Origin', origin)
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res

def make_json_response(json, res):
    json.headers = res.headers
    json.headers.set('Content-Type', 'application/json')
    return json