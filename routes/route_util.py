import os

from flask import current_app, jsonify
from werkzeug.utils import secure_filename

def create_response(status, desc = "", data = []):
    return jsonify({ 'status': status, 'desc' : desc, 'data': data })

def allowed_extensions(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def save_image(img):
    image_dir = current_app.config['DIR']['images']
    extensions = current_app.config['DIR']['extensions']

    if img and allowed_extensions(img.filename, extensions):
        print('allowed ext')
        filename = secure_filename(img.filename)
        
        try:
            img.save(os.path.join(image_dir, filename))
        except Exception as error:
            filename = ''
            print(f"WARN: unable to successfully save {filename} to disk.")
            print(jsonify(error))
        return filename
    else:
        return ''