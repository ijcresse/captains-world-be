from flask import Flask, request

#from services.db import create_connection
#from routes.health import create_response
from routes.health import health_api

def create_app(config = None):
    app = Flask(__name__)

    app.register_blueprint(health_api)

    return app



# @app.route("/drink/list", methods=['GET'])
# def drink_list():
#     limit = request.args.get('limit') if request.args.get('limit') is not None else 20
#     offset = request.args.get('offset') if request.args.get('offset') is not None else 0

#     connection = create_connection()
#     cursor = connection.cursor()
#     query = f"SELECT c_id, c_name, c_type, c_date_crafted, c_image_url FROM t_drink LIMIT {limit} OFFSET {offset}"
#     print(query)
    
#     cursor.execute(query)
#     result = cursor.fetchall()
#     connection.close()
#     return create_response(status = 200, data = [result])
#     #check for errors

# #GET /drink/description
# #queryparams: id (required)
# #gets detailed info about given drink ID
# @app.route("/drink/description", methods=['GET'])
# def drink_desc():
#     id = request.args.get('id')
#     if id is None:
#         return create_response(status = 400, desc = "missing id parameter")
    
#     connection = create_connection()
#     cursor = connection.cursor()
#     query = f"SELECT c_name, c_type, c_date_crafted, c_image_url FROM t_drink WHERE c_id={id}"
    
#     cursor.execute(query)
#     result = cursor.fetchone()
#     connection.close()

#     #check for errors

#     return create_response(status = 200, data = [result])



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