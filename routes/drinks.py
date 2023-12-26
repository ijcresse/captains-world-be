from flask import Blueprint, request, jsonify

from .route_util import save_image, is_authorized, _build_cors_preflight_response, _make_cors_response
from services.db import get_db, close_db
from models.drink import Drink

drinks_api = Blueprint('drink', __name__, url_prefix = '/api/drink')

#GET /drink/detail/<id>
#queryparams: id (required)
#gets detailed info about given drink ID
@drinks_api.route("/detail/<id>", methods=['GET', 'OPTIONS'])
def drink_desc(id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    if id is None:
        res.status = 400
        res.set_data('Missing ID')
        return res
    
    c = get_db()
    cursor = c.cursor()
    query = Drink.get_drink_query(id)
    
    cursor.execute(query)
    result = cursor.fetchone()
    close_db(c)

    #check for errors, adjust response as necessary
    json = jsonify(result)
    json.headers = res.headers
    return json

#PUT /drink/detail/<id>/edit
#queryparams: id (requred)
#updates drink information based on what's present.
@drinks_api.route("/detail/<id>/edit", methods=['PUT', 'OPTIONS'])
def update_drink(id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    if not is_authorized():
        res.status = 401
        res.set_data('Secured endpoint')
        return res

    if id is None:
        res.status = 400
        res.set_data('Missing ID')
        return res
    
    data = request.get_json()
    try:
        drink = Drink(data)
    except:
        res.status = 400
        res.set_data('One or more parameters is malformed or missing.')
        return res
    
    c = get_db()
    cursor = c.cursor()
    query = drink.update_drinks_query(id, drink)
    cursor.execute(query)
    c.commit()
    close_db(c)

    res.status = 200
    return res
        
#GET /drink/list
#queryparams: limit, offset
#gets data and metadata about various drinks. default 20 drinks, max 50 per request.
@drinks_api.route("/list", methods=['GET', 'OPTIONS'])
def drink_list():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    limit = int(request.args.get('limit')) if request.args.get('limit') is not None else 12
    offset = int(request.args.get('offset')) if request.args.get('offset') is not None else 0
    limit = 50 if limit > 50 else limit
    
    connection = get_db()
    cursor = connection.cursor()

    query = Drink.get_drinks_query(limit, offset)
    print(query)
    
    cursor.execute(query)
    result = cursor.fetchall()
    close_db()
    
    json = jsonify(result)
    json.headers = res.headers
    return json

#GET /drink/list/count
#returns a number representing the total drinks in the database.
#use for calculating pagination
@drinks_api.route("/list/count", methods=['GET', 'OPTIONS'])
def count_drinks():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    c = get_db()
    cursor = c.cursor()
    query = Drink.count_drinks_query()

    cursor.execute(query)
    result = cursor.fetchone()
    close_db(c)
    
    json = jsonify({'count' : result['count(c_id)']})
    json.headers = res.headers
    return json

#POST /drink/new
#request object: drink (required)
#posts a new drink object. returns an ID on success with which an image can be posted to.
@drinks_api.route("/new", methods=['POST', 'OPTIONS'])
def post_drink():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    if not is_authorized():
        res.status = 401
        res.set_data('Secured endpoint')
        return res

    #process drink object from request
    if request.is_json is False:
        res.status = 400
        res.set_data('Missing drink data')
        return res
    
    data = request.get_json()
    try:
        drink = Drink(data)
    except:
        res.status = 400
        res.set_data('One or more parameters is malformed or missing.')
        return res

    c = get_db()
    cursor = c.cursor()
    query = drink.post_drink_query()
    cursor.execute(query)
    c.commit()

    #expecting requests to be user driven, extremely unlikely for concurrency issues
    #but this might be a good place to improve things. TODO
    get_id = "SELECT c_id, c_name FROM t_drink ORDER BY c_id DESC LIMIT 1"
    cursor.execute(get_id)
    row = cursor.fetchone()
    close_db(c)
    
    if row['c_name'] == drink.name:
        json = jsonify({'c_id' : row['c_id']})
        json.headers = res.headers
        return json
    else:
        res.status = 500
        res.set_data(f"unable to post drink {drink.name} to db")
        return res
    
#post image. follow up API to the POST drink metadata endpoint, requires ID returned from that
@drinks_api.route("/img/<id>", methods=['POST', 'OPTIONS'])
def post_drink_image(id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    if not is_authorized():
        res.status = 401
        res.set_data("Secured endpoint")
        return res

    if 'file' not in request.files or request.files['file'].filename == '':
        res.status = 400
        res.set_data("Missing image file")
        return res

    img = request.files['file']

    filename = save_image(id, img)
    if filename is None or filename == '':
        res.status = 500
        res.set_data("Unable to save image to disk")
        return res
    else:
        c = get_db()
        cursor = c.cursor()
        query = Drink.post_drink_image_query(filename, id)
        print(query)
        cursor.execute(query)
        c.commit()
        close_db(c)

        #what if this fails, or get a bad id?
        res.set_data(f"saved {filename} to disk")
        return res