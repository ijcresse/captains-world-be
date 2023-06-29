from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"

#GET /drink/list
#queryparams: limit offset (not required)
#gets say, latest 20 drinks along with material needed for display in FE

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
#request object: drink_request. full of details and params.
#for admin, requires cookie
#stores image elsewhere and fetches image id, stores that in db. unsure exactly how this works

#PUT /drink/description
#for admin, requires cookie
#updates a given drink with an updated drink object. detects whether image is same. need to figure that one out

#PUT /contact
#for admin, requires cookie
#updates contact info for captain

#GET /health
#GET /availability