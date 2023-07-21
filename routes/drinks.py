import os
from flask import Blueprint, request

from .route_util import create_response, save_image
from services.db import get_db, close_db
from models.drink import Drink

drinks_api = Blueprint('drink', __name__, url_prefix = '/api/drink')

#GET /drink
#queryparams: id (required)
#gets detailed info about given drink ID
@drinks_api.route("/<id>", methods=['GET'])
def drink_desc(id):
    if id is None:
        return create_response(status = 400, desc = "missing id")
    
    c = get_db()
    cursor = c.cursor()
    query = f"SELECT c_name, c_type, c_date_crafted, c_image_url FROM t_drink WHERE c_id={id}"
    
    cursor.execute(query)
    result = cursor.fetchone()
    close_db(c)

    #check for errors, adjust response as necessary

    return create_response(status = 200, data = [result])

#POST /drink/
#request object: drink (required)
#posts a new drink object. returns an ID on success with which an image can be posted to.
@drinks_api.route("/", methods=['POST'])
def post_drink():
    #process drink object from request
    if request.is_json is False:
        return create_response(status = 400, desc = "missing drink data")
    data = request.get_json()
    print(data)

    drink = Drink(data)

    #create db connection, save drink object to database. fetch ID of inserted row
    c = get_db()
    cursor = c.cursor()
    query = drink.post_drink_query()
    cursor.execute(query)
    c.commit()

    get_id = "SELECT c_id, c_name FROM t_drink ORDER BY c_id DESC LIMIT 1"
    cursor.execute(get_id)
    row = cursor.fetchone()
    
    if row['c_name'] == drink.name:
        create_response(status = 200, data = { 'id' : id})
    else:
        create_response(status = 500, desc = f"unable to post drink {drink.name} to db")
    

@drinks_api.route("/<id>/img", methods=['POST'])
def post_drink_image(id):
    if 'file' not in request.files or request.files['file'].filename == '':
        return create_response(status = 400, desc = "missing image file")

    img = request.files['file']

    filename = save_image(img)
    if filename == '':
        create_response(status = 500, desc = "unable to save image to disk")
    else:
        create_response(status = 200, desc = f"saved {filename} to disk")


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
