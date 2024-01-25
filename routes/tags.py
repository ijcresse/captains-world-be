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
    
    if request.is_json is False:
        res.status = 400
        res.set_data('Missing tag data')
        return res
    
    data = request.get_json()
    tags = []
    try:
        for element in data:
            tags.append(Tag(element))
    except:
        res.status = 400
        res.set_data('One or more tags could not be processed')
        return res
    
    #rest
    

#helper method to diff a given review's current tags against update tags
def find_delta(review_id, new_tags, cursor):
    #getting tags from review id
    query = Tag.get_tags_from_review_query(review_id)
    cursor.execute(query)
    #db tags are { c_id, c_tag_name }. can't normalize down to c_tag_name...
    #can i make new_tags with blank c_ids?
    db_tags = cursor.fetchall()
    #comparing that against tags list

    #two runners. when a match is found, remove from both.
    #what's left in db_tags are REMOVALS
    #what's left in new_tags are ADDITIONS
    i = 0
    j = 0
    while (i < len(db_tags)):
        if (db_tags[i].c_tag_name == new_tags[j]):
            db_tags.pop(i)
            new_tags.pop(j)
        if (j == len(new_tags)):
            i = i + 1
            j = 0
        else:
            j = j + 1

    #send db_tags leftovers to deletion helper
    #send new_tags leftovers to addition helper
    return 0

#adds a tag to the tag table

#deletes a tag from the tag table

#adds a drink_tag to the drink_tag table

#deletes a drink_tag from the linking table