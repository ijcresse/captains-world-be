from flask import Flask, request
import pymysql.cursors
import os

def create_connection():
    return pymysql.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        database = os.getenv("DB_NAME"),
        cursorclass = pymysql.cursors.DictCursor
    )

app = Flask(__name__)
#connection = create_connection()

@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"

#GET /drink/list
#queryparams: limit offset (not required)
#gets say, latest 20 drinks along with material needed for display in FE

@app.route("/health", methods=['GET'])
def health():
    return "OK"

@app.route("/availability", methods=['GET'])
def availability():
    return "OK"

@app.route("/drink/list", methods=['GET'])
def drink_list():
    limit = request.args.get('limit') if request.args.get('limit') is not None else 50
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0
    #establish connection
    #SELECT c_id, c_name, c_type, c_date_crafted, c_image_url
    #commit, fetchall
    #check for errors
    #

#GET /drink/description
#queryparams: id (required)
#gets detailed info about given drink ID

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
#stores image elsewhere and fetches image id, stores that in db. unsure exactly how this works

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