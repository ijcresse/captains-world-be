import os

from datetime import datetime, timedelta
from flask import current_app, jsonify, session
from werkzeug.utils import secure_filename

from models.user import User
from services.db import get_db, close_db

def create_response(status, desc = "", data = []):
    return jsonify({ 'desc' : desc, 'data': data }), status

def allowed_extensions(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def save_image(id, img):
    image_dir = current_app.config['DIR']['images']
    extensions = current_app.config['DIR']['extensions']

    if img and allowed_extensions(img.filename, extensions):
        filename = secure_filename(f"{id}_{img.filename}")
        
        try:
            img.save(os.path.join(image_dir, filename))
        except Exception as error:
            filename = ''
            print(f"WARN: unable to successfully save {filename} to disk.")
            print(jsonify(error))
        return filename
    else:
        return ''

#checks if the current session is authorized. deletes if the session is expired.
def is_authorized():
    if 'cw-session' in session:
        session_name = session['cw-session']
        c = get_db()
        cursor = c.cursor()
        query = User.fetch_session(session_name)
        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            close_db(c)
            return False
        else:
            if session_is_active(result['c_login_time']):
                close_db(c)
                return True
            else:
                delete_session(session_name, c)
                return False

def session_is_active(login_time):
    login_duration_env = current_app.config['DB']['session_timeout']
    login_duration = datetime.strptime(login_duration_env, '%H:%M:%S')
    logout_time = login_time + timedelta(hours = login_duration.hour)
    current_time = datetime.now()
    return logout_time > current_time

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

        session.pop('cw-session', None)

        return True

