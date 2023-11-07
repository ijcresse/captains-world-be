from flask import Blueprint, request

from flask_cors import CORS
from .route_util import create_response, save_image, is_authorized
from services.db import get_db, close_db
from models.drink import Drink

drinks_api = Blueprint('drink', __name__, url_prefix = '/api/drink')
CORS(drinks_api, resources = {r'/api/*': {"origins": "http://localhost:5173"}})

#GET /drink
#queryparams: id (required)
#gets detailed info about given drink ID
@drinks_api.route("/<id>", methods=['GET'])
def drink_desc(id):
    if id is None:
        return create_response(status = 400, desc = "missing id")
    
    c = get_db()
    cursor = c.cursor()
    query = Drink.get_drink_query(id)
    
    cursor.execute(query)
    result = cursor.fetchone()
    close_db(c)

    #check for errors, adjust response as necessary

    return create_response(status = 200, data = [result])

#POST /drink/new
#request object: drink (required)
#posts a new drink object. returns an ID on success with which an image can be posted to.
@drinks_api.route("/new", methods=['POST'])
def post_drink():
    print('post drink')
    if not is_authorized():
        return create_response(status = 401, desc = "secured endpoint")

    #process drink object from request
    if request.is_json is False:
        return create_response(status = 400, desc = "missing drink data")
    data = request.get_json()
    drink = Drink(data)

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
        return create_response(status = 200, data = {'id' : row['c_id']})
    else:
        return create_response(status = 500, desc = f"unable to post drink {drink.name} to db")
    
#post image. follow up API to the POST drink metadata endpoint, requires ID returned from that
@drinks_api.route("/new/<id>/img", methods=['POST'])
def post_drink_image(id):
    if not is_authorized():
        return create_response(status = 401, desc = "secured endpoint")

    if 'file' not in request.files or request.files['file'].filename == '':
        return create_response(status = 400, desc = "missing image file")

    img = request.files['file']

    filename = save_image(id, img)
    if filename is None or filename == '':
        return create_response(status = 500, desc = "unable to save image to disk")
    else:
        c = get_db()
        cursor = c.cursor()
        query = Drink.post_drink_image_query(filename, id)
        print(query)
        cursor.execute(query)
        c.commit()
        close_db(c)
        #what if this fails, or get a bad id?

        return create_response(status = 200, desc = f"saved {filename} to disk")


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

    query = Drink.get_drinks_query(limit, offset)
    print(query)
    
    cursor.execute(query)
    result = cursor.fetchall()
    close_db()
    
    return create_response(status = 200, data = [result])
    #check for errors
