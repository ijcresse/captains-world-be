from flask import Blueprint, request, jsonify
from .route_util import is_authorized, unauthorized_response, _build_cors_preflight_response, _make_cors_response, get_db, close_db
from models.tag import Tag

tags_api = Blueprint('tags', __name__, url_prefix = '/api/tags')

#GET /tags/for/review/<review id>
#queryparams: review id (required)
#gets list of tags associated with a given review id
@tags_api.route("/for/review/<review_id>", methods=['GET', 'OPTIONS'])
def get_tags_for_review(review_id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response(request.origin)
    
    res = _make_cors_response(request.origin)

    connection = get_db()
    cursor = connection.cursor()
    query = Tag.get_tags_from_review_query(review_id)
    cursor.execute(query)
    result = cursor.fetchall()
    close_db()

    res.status = 200
    res.set_data(result)
    return res

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
        return unauthorized_response(res)
    
    if request.is_json is False:
        res.status = 400
        res.set_data('Missing tag data')
        return res
    
    tags = request.get_json()
    if len(tags) == 0:
        res.status = 400
        res.set_data("No tags to process")
        return res
    
    connection = get_db()
    cursor = connection.cursor()

    (add_tags, delete_tags) = find_delta(review_id, tags, cursor)
    if len(add_tags) > 0:
        commit_tags_to_db(add_tags, review_id, connection, cursor)
    if len(delete_tags) > 0:
        remove_tags_from_db(delete_tags, review_id, connection, cursor)

    close_db()

    res.status = 200
    return res

#helper method to diff a given review's current tags against update tags.
def find_delta(review_id, new_tags, cursor):
    query = Tag.get_tags_from_review_query(review_id)
    cursor.execute(query)

    db_tags = cursor.fetchall()

    i = 0
    j = 0
    while (i < len(db_tags)):
        if (db_tags[i]['c_tag_name'] == new_tags[j]):
            db_tags.pop(i)
            new_tags.pop(j)
            if i > 0:
                i = i - 1
            if j > 0:
                j = j - 1
        elif (j == len(new_tags) - 1):
            i = i + 1
            j = 0
        else:
            j = j + 1

    return (new_tags, db_tags)

#helper method to process tags to add to a review. prevents overlapping.
def commit_tags_to_db(tags, review_id, connection, cursor):
    new_tag_ids = []
    existing_tag_ids = []
    for tag in tags:
        id = get_tag_id(tag, cursor)
        if id is None:
            new_tag_ids.append(tag)
        else:
            existing_tag_ids.append({'c_id': id['c_id'], 'c_tag_name': tag})
    
    for tag in new_tag_ids:
        add_tag(tag, cursor)
        connection.commit()
        tag_id = get_tag_id(tag, cursor)
        add_tag_to_review(tag_id['c_id'], review_id, cursor)
    connection.commit()
    for tag in existing_tag_ids:
        add_tag_to_review(tag['c_id'], review_id, cursor)
    connection.commit()

#checks for straggler tags and deletes them
def remove_tags_from_db(tags, review_id, connection, cursor):
    for tag in tags:
        tag_id = tag['c_id']
        delete_tag_from_review(tag_id, review_id, cursor)
        connection.commit()

        query = Tag.check_last_tag_query(tag_id)
        cursor.execute(query)
        result = cursor.fetchone()
        if result['COUNT(*)'] == 0:
            delete_tag(tag_id, cursor)
            connection.commit()

#fetches tag_id for a given tag_name from the tag table
def get_tag_id(tag_name, cursor):
    query = Tag.get_tag_query(tag_name)
    cursor.execute(query)
    return cursor.fetchone()

#adds a tag to the tag table
def add_tag(tag_name, cursor):
    query = Tag.post_tag_query(tag_name)
    cursor.execute(query)

#deletes a tag from the tag table
def delete_tag(tag_id, cursor):
    query = Tag.delete_tag_query(tag_id)
    cursor.execute(query)

#adds a drink_tag to the drink_tag table
def add_tag_to_review(tag_id, review_id, cursor):
    query = Tag.post_drink_tag_query(tag_id, review_id)
    cursor.execute(query)

#deletes a drink_tag from the linking table
def delete_tag_from_review(tag_id, review_id, cursor):
    query = Tag.delete_drink_tag_query(tag_id, review_id)
    cursor.execute(query)