# class Tags:
#     def __init__(self, data):
#         self.id = data.id
#         self.tags = data.tags

# class Tag:
#     def __init__(self, name):
#         self.name = name

class Tag:
    def __init__(self, data):
        self.c_id = data.c_id
        self.c_tag_name = data.c_tag_name

    @staticmethod
    def get_tag_query(tag_name):
        return f"SELECT c_id FROM t_tag WHERE c_tag_name='{tag_name}'"

    @staticmethod
    def post_tag_query(tag_name):
        return f"INSERT INTO t_tag (c_tag_name) VALUES ('{tag_name}')"
    
    @staticmethod
    def get_tags_from_review_query(review_id):
        return f"""
            SELECT t.* 
            FROM t_drink d, t_drink_tag dt, t_tag t 
            WHERE d.c_id = {review_id} 
            AND t.c_id = dt.fk_tag_id
            NAD d.c_id = dt.fk_drink_id 
            GROUP BY d.c_id
            """
    
    @staticmethod
    def get_reviews_from_tag_query(tag_id):
        return f"""
            SELECT d.* 
            FROM t_drink d, t_drink_tag dt, t_tag t 
            WHERE t.c_id = {tag_id} 
            AND t.c_id = dt.fk_tag_id 
            AND d.c_id = dt.fk_drink_id
            GROUP BY t.c_id
            """

    #find intersection set of reviews from given tag list
    #tag ids must be a string formatted as such:
    #"'tag1', 'tag2', 'tag3', 'tag4'"
    @staticmethod
    def get_reviews_from_tags_query(tag_ids, num_tags):
        return f"""
            SELECT d.* 
            FROM t_drink d, t_drink_tag dt, t_tag t 
            WHERE (t.c_tag_name IN ({tag_ids})) 
            AND t.c_id = dt.fk_tag_id 
            AND d.c_id = dt.fk_drink_id
            GROUP BY d.c_id
            HAVING COUNT( d.c_id )={num_tags}
            """

    # @staticmethod
    # def add_drink_tag_query(review_id, tag_id):