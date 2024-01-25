from flask import Blueprint, request, jsonify
from .route_util import is_authorized, unauthorized_response, _build_cors_preflight_response, _make_cors_response
from models.tag import Tag

tags_api = Blueprint('tags', __name__, url_prefix = '/api/tags')

#GET /tags/for/review/<review id>
#queryparams: review id (required)
#gets list of tags associated with a given review id

#GET /tags/list/reviews/<tag id>
#queryparams: tag id (required)
#gets list of review IDs associated with a given tag

#POST /tags/for/review/<review id>
#queryparams: review id (required)
#request object: tag[] (required)
#posts a list of tags associated with a given review id
@tags_api.route("/for/review/<review_id>", methods=['POST', 'OPTIONS'])
def post_tags_for_review(review_id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    if not is_authorized():
        return unauthorized_response
    
    
    

#helper method to diff a given review's current tags against update tags

#adds a tag to the tag table

#deletes a tag from the tag table

#adds a drink_tag to the drink_tag table

#deletes a drink_tag from the linking table