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
    
    # @staticmethod
    # def add_drink_tag_query(review_id, tag_id):