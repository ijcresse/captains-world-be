from flask import Blueprint, request, current_app
from .route_util import create_response
from services.db import get_db, close_db

drinks_api = Blueprint('drink', __name__, url_prefix = '/api/drink')

#GET /drink
#queryparams: id (required)
#gets detailed info about given drink ID
@drinks_api.route("/", methods=['GET'])
def drink_desc():
    id = request.args.get('id')
    if id is None:
        return create_response(status = 400, desc = "missing id parameter")
    
    connection = get_db()
    cursor = connection.cursor()
    query = f"SELECT c_name, c_type, c_date_crafted, c_image_url FROM t_drink WHERE c_id={id}"
    
    cursor.execute(query)
    result = cursor.fetchone()
    close_db(connection)

    #check for errors

    return create_response(status = 200, data = [result])

#POST /drink/
@drinks_api.route("/", methods=['POST'])
def post_drink():
    image_dir = current_app.config['DIR']['images']
    if 'file' not in request.files:
        

#GET /drink/list
#queryparams: limit, offset
#gets data and metadata about various drinks. default 20 drinks, max 50 per request.
@drinks_api.route("/list", methods=['GET'])
def drink_list():
    limit = request.args.get('limit') if request.args.get('limit') is not None else 20
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0

    limit = 50 if limit > 50 else limit
    
    connection = get_db()
    cursor = connection.cursor()
    query = f"SELECT c_id, c_name, c_type, c_date_crafted, c_image_url FROM t_drink LIMIT {limit} OFFSET {offset}"
    print(query)
    
    cursor.execute(query)
    result = cursor.fetchall()
    close_db()
    return create_response(status = 200, data = [result])
    #check for errors
