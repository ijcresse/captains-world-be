def create_response(status, desc = "", data = []):
    return { 'status': status, 'desc' : desc, 'data': data }

def allowed_extensions(filename, extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in extensions