from flask import Blueprint, request, jsonify
from .route_util import _make_json_response, _build_cors_preflight_response, _make_cors_response, get_db, close_db
from models.search_query import SearchQuery
from models.tag import Tag

search_api = Blueprint('search', __name__, url_prefix = '/api/search')

@search_api.route("", methods=['GET', 'OPTIONS'])
def search():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    name = request.args.get('c_name')
    type = request.args.get('c_sake_type')

    review_ids = []
    if request.is_json:
        tags = request.get_json()
        review_ids = search_on_tags(tags, name, type)
    elif name is not None or type is not None:
        review_ids = search_on_params(name, type)
    else:
        res.status = 400
        res.set_data("Missing search query params and tags")
        return res

    json = jsonify(review_ids)
    return _make_json_response(json, res)

def search_on_tags(tags, name, type):
    connection = get_db()
    cursor = connection.cursor()
    
    tag_ids = get_ids_for_tags(tags, cursor)
    query = SearchQuery.get_reviews_from_tags_query(tag_ids)

    cursor.execute(query)
    reviews = cursor.fetchall()

    if type is not None:
        i = 0
        while i < len(reviews):
            if reviews[i]['c_sake_type'].lower() == type:
                i = i + 1
            else:
                reviews.pop(i)
    
    if name is not None:
        i = 0
        while i < len(reviews):
            if name in reviews[i]['c_name'].lower():
                i = i + 1
            else:
                reviews.pop(i)
    
    close_db(connection)

    return reviews


def search_on_params(name, type):
    connection = get_db()
    cursor = connection.cursor()
    
    query = SearchQuery.get_reviews_from_params_query(name, type)
    cursor.execute(query)
    reviews = cursor.fetchall()

    close_db(connection)
    
    return reviews

def get_ids_for_tags(tags, cursor):
    tag_ids = []
    for tag in tags:
        query = Tag.get_tag_query(tag)
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            tag_ids.append(result)
    return tag_ids