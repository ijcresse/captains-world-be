def create_response(status, desc = "", data = []):
    return { 'status': status, 'desc' : desc, 'data': data }

def allowed_extensions(filename, extensions):
    print(f"allowed_extensions check. name of file: {filename}. ext: {filename.rsplit('.')[1].lower()}")
    test = filename.rsplit('.')[1].lower()
    test2 = test in extensions
    print(f"is filename in extensions list? {test2}")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions